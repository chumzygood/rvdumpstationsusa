"""Capture public, location-specific official source evidence for additional listings."""
from pathlib import Path
import requests,json,hashlib,re
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
records=[];audit=[]
def fetch(url,key):
 
 if 'usace.army.mil' in url:
  snapshot='research/'+key+'-official-excerpt.html'
  raw=(ROOT/snapshot).read_text();soup=BeautifulSoup(raw,'html.parser')
  return soup,soup.get_text(' ',strip=True),{'url':url,'snapshot':snapshot,'sha256':hashlib.sha256(raw.encode()).hexdigest(),'capture_method':'Curated excerpts from official WebFetch response; direct requests returned 403.'}
 r=requests.get(url,timeout=35);r.raise_for_status();r.encoding=r.apparent_encoding
 soup=BeautifulSoup(r.text,'html.parser');text=soup.get_text(' ',strip=True)
 snapshot='research/'+key+'.txt';(ROOT/snapshot).write_text(text)
 return soup,text,{'url':r.url,'snapshot':snapshot,'sha256':hashlib.sha256(text.encode()).hexdigest()}
def base(id,name,operator,typ,city,street,zip,source,evidence):
 return {'id':id,'property_name':name,'name':name+' — RV dump station','operator':operator,'source_type':typ,'state':'Texas','state_code':'TX','city':city,'address':{'street':street,'city':city,'region':'TX','postal_code':zip,'country':'US','precision':'Operator property address; verify the dump-station entrance.' if street else 'Street address not confirmed. This is a lake-area listing, not a municipal-city or precise-entrance claim; follow the official operator directions.'},'last_checked':'2026-11-10','verification_scope':'Official operator lists the dump-station amenity. Not an on-site inspection or confirmation that it is open today. One record per property, not per lane or physical outlet.','park_status':'Operating status not confirmed; check operator','alerts':[],'source_url':source['url'],'operator_url':source['url'],'sources':[dict(source,type=typ,supports=['dump_station','location'],evidence=evidence)]}
for num in [270,610,475]:
 url=f'https://www.loves.com/locations/{num}'
 soup,text,src=fetch(url,'loves-'+str(num))
 assert 'RV Dump Service' in text
 ld=json.loads(soup.select_one('script[type="application/ld+json"]').string);a=ld['address']
 records.append(base('loves-'+str(num),"Love’s Travel Stop #"+str(num),'Love’s Travel Stops','travel_center_operator',a['addressLocality'],a['streetAddress'],a['postalCode'],src,'Location-specific amenities list: RV Dump Service. Store hours and general payment types are not assumed to apply to dumping.'))
for city in ['rockwall','ganado','dallas-south']:
 url=f'https://www.ta-petro.com/location/tx/ta-{city}/'
 try:
  soup,text,src=fetch(url,'ta-'+city)
  assert 'RV Dump' in text,'No location-specific RV Dump amenity found'
  ld=next(json.loads(x.get_text()) for x in soup.select('script[type="application/ld+json"]') if 'streetAddress' in x.get_text());a=ld['address']
  records.append(base('ta-'+city,ld['name'],'TravelCenters of America','travel_center_operator',a['addressLocality'],a['streetAddress'],a['postalCode'],src,'Location amenities include RV Dump.'))
 except Exception as ex:audit.append({'url':url,'result':'Not added','reason':str(ex)})
for lake,names in [('belton',['Cedar Ridge Park','Live Oak Ridge Park','Westcliff Park','White Flint Park']),('canyon',['Cranes Mill Park','Potters Creek Park'])]:
 url=f'https://www.swf-wc.usace.army.mil/{lake}/Recreation/Parks/Corpsparks.shtml'
 soup,text,src=fetch(url,'usace-'+lake)
 for name in names:
  h=next(x for x in soup.select('h2') if x.get_text(' ',strip=True)==name)
  parts=[]
  for el in h.next_siblings:
   if getattr(el,'name',None)=='h2':break
   if hasattr(el,'get_text'):parts.append(el.get_text(' ',strip=True))
  section=' '.join(parts);assert re.search(r'dump station',section,re.I),name
  id='usace-'+lake+'-'+re.sub('[^a-z0-9]+','-',name.lower()).strip('-')
  rec=base(id,name+' — '+('Belton Lake' if lake=='belton' else 'Canyon Lake'),'U.S. Army Corps of Engineers','federal_usace',('Belton Lake area' if lake=='belton' else 'Canyon Lake area'),None,None,src,section)
  # Avoid claiming the dump facility is usable when its campground is seasonally closed.
  if name in ['Westcliff Park','White Flint Park']:
   rec['alerts']=[{'text':'USACE states this park closes for winter from November 1 through March 1; the boat ramp remaining open does not confirm dump-station access. Check with the operator before travel.','url':src['url']}]
  records.append(rec)
(ROOT/'research/additional-stations.json').write_text(json.dumps(records,indent=2,ensure_ascii=False)+'\n')
(ROOT/'research/additional-source-audit.json').write_text(json.dumps(audit,indent=2)+'\n')
print('Added verified official-source records:',len(records));print(json.dumps(audit,indent=2))
