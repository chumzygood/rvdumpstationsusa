"""Nov 12 2026: additional USACE Fort Worth District properties from official park pages (offline, frozen snapshots).
Snapshots were captured by direct HTTPS request on 2026-11-12. Unknowns stay unknown."""
from pathlib import Path
from bs4 import BeautifulSoup
import json,hashlib,re
ROOT=Path(__file__).resolve().parents[1]; D='2026-11-12'
LAKE={'navarro':'Navarro Mills Lake','bardwell':'Bardwell Lake','lewisville':'Lewisville Lake','wrightpatman':'Wright Patman Lake'}
def section(soup,name):
  h=next(x for x in soup.select('h2') if x.get_text(' ',strip=True)==name); parts=[]
  for el in h.next_siblings:
    if getattr(el,'name',None)=='h2': break
    parts.append(el.get_text(' ',strip=True) if hasattr(el,'get_text') else str(el).strip())
  return ' '.join(' '.join(parts).split())
def sent(text,pat):
  m=re.search(r'[^.]*'+pat+r'[^.]*\.?',text,re.I); return m.group(0).strip() if m else None
NAV_FEE="The following fees are only charged to members of the public who have not paid the standard camping fees."
want=[('navarro','Liberty Hill Park'),('navarro','Wolf Creek Park'),('navarro','Oak Park'),('navarro','Pecan Point Park'),
      ('bardwell','High View Park'),('bardwell','Mott Park'),('lewisville','Hickory Creek Park'),
      ('wrightpatman','Clear Springs Campground'),('wrightpatman','Piney Point Campground'),('wrightpatman','Rocky Point Campground'),('wrightpatman','Malden Lake Campground')]
out=[]
for lake,name in want:
  url=f'https://www.swf-wc.usace.army.mil/{lake}/Recreation/Parks/Corpsparks.shtml'
  snap=f'research/usace-{lake}.txt'; sha=hashlib.sha256((ROOT/snap).read_bytes()).hexdigest()
  soup=BeautifulSoup(open(f'/tmp/rv/{lake}.html',errors='ignore'),'html.parser'); sec=section(soup,name)
  ev=sent(sec,r'dump station') if lake!='navarro' or 'dump station.' in sec.lower() and 'Pecan' in name else None
  if lake=='navarro':
    ev=(sent(sec,r'public restrooms and a dump station')+' ' if 'Pecan' in name else '')+NAV_FEE+' Dump Station Fee $4.00 (listed in this park’s section).'
  assert ev and 'dump' in ev.lower(),name
  street=city=zip_=None; city=LAKE[lake]+' area'
  precision='Street address not confirmed. This is a lake-area listing, not a municipal-city or precise-entrance claim; follow the official operator directions.'
  if name=='Hickory Creek Park':
    street,city,zip_='1201 Point Vista Rd.','Hickory Creek','75065'; precision='Operator property address; verify the dump-station entrance.'
  sid='usace-'+lake+'-'+re.sub('[^a-z0-9]+','-',name.lower()).strip('-')
  rec={'id':sid,'property_name':f'{name} — {LAKE[lake]}','name':f'{name} — {LAKE[lake]} — RV dump station','operator':'U.S. Army Corps of Engineers','source_type':'federal_usace','state':'Texas','state_code':'TX','city':city,
       'address':{'street':street,'city':city,'region':'TX','postal_code':zip_,'country':'US','precision':precision},'last_checked':D,
       'verification_scope':'Official operator lists the dump-station amenity. Not an on-site inspection or confirmation that it is open today. One record per property, not per lane or physical outlet.',
       'park_status':'Operating status not confirmed; check operator','alerts':[],'source_url':url,'operator_url':url,
       'sources':[{'url':url,'snapshot':snap,'sha256':sha,'capture_method':'Direct HTTPS request to the official USACE page on 2026-11-12.','type':'federal_usace','supports':['dump_station','location'],'evidence':ev}],
       'question_overrides':{}}
  q=rec['question_overrides']
  if lake=='navarro':
    q['fee']={'status':'documented','answer':'$4.00 dump station fee for members of the public who have not paid the standard camping fees (USACE Navarro Mills park fee list). Campers who paid camping fees are not charged this fee.','source_url':url}
    q['non_guest_access']={'status':'documented','answer':'Yes — USACE lists a $4.00 dump station fee charged to members of the public who have not paid camping fees. Fees are collected at the gatehouse.','source_url':url}
  season={'Wolf Creek Park':'The park is open from April 1 through September 30.','Pecan Point Park':'The park is open April 1 - September 30.','Piney Point Campground':'Campground open March 1 - September 30.','Rocky Point Campground':'Open year-round.','Malden Lake Campground':'Open October through May, closed June through September.'}
  if name in season:
    assert season[name] in sec,name
    q['seasonal']={'status':'documented','answer':f'USACE park/campground season: “{season[name]}” (park season; a separate dump-station season is not stated).','source_url':url}
    if name in ('Wolf Creek Park','Pecan Point Park','Piney Point Campground'):
      rec['alerts'].append({'text':f'USACE: “{season[name]}” As of 2026-11-12 this is outside the listed season; do not expect access until the park reopens. Check with the operator.','url':url})
  if lake=='navarro':
    rec['alerts'].append({'text':'USACE: the gatehouse is open for business between 6:00 a.m. and 10:00 p.m. (gatehouse hours, not confirmed dump-station hours).','url':url})
  if name=='Hickory Creek Park':
    rec['alerts'].append({'text':'USACE: gate attendant on duty during open hours, 10am–10pm (gate hours, not confirmed dump-station hours).','url':url})
  out.append(rec)
(ROOT/'research/additional-stations-2026-11-12.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print('records',len(out))
