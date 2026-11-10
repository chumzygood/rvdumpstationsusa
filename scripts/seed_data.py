"""Create deterministic station data from checked-in official evidence (offline)."""
from pathlib import Path
import json,html
ROOT=Path(__file__).resolve().parents[1]
CHECKED='2026-11-10'
INDEX='https://tpwd.texas.gov/state-parks/parks-map'
QUESTIONS={
 'fee':'What does dumping cost?',
 'potable_water':'Can I fill my drinking-water tank?',
 'non_guest_access':'Can I use it without camping here?',
 'seasonal':'Is the dump station seasonal?',
 'hours':'What are the dump-station hours?',
 'payment':'Which payment methods are accepted?',
 'big_rig_access':'Will my large RV fit at the dump station?'}
def answer(text=None,url=None):
 return {'status':'documented' if text else 'unknown','answer':text or 'Not confirmed in the checked official sources. Verify with the operator before traveling.','source_url':url}
def main():
 parks=json.loads((ROOT/'research/texas-official.json').read_text())
 audits={x['slug']:x for x in json.loads((ROOT/'research/source-audit.json').read_text())}
 stations=[]
 for p in parks:
  if p['idname'] not in audits:continue
  loc=p['location'];audit=audits[p['idname']]
  home=next((v for v in audit['pages'] if v['url']==p['url'] and not v.get('error')),None)
  if not home:continue
  facts={k:answer() for k in QUESTIONS}
  sources=[{'url':INDEX,'type':'state_park_agency','supports':['dump_station','name','address','city','park_status'],'evidence':f"TPWD public park-directory record idname={p['idname']}; amenities contains dump_station. This verifies a listed facility, not live availability.",'snapshot':'research/texas-official.json'}]
  for page in audit['pages']:
   if page.get('error'):continue
   sources.append({'url':page['url'],'type':'state_park_agency','supports':['park_information'],'snapshot':page['snapshot'],'sha256':page['sha256'],'dump_mentions':page['dump_mentions']})
   if page['dump_fee_blocks']:
    facts['fee']=answer(' '.join(page['dump_fee_blocks'])+' Park admission may be additional; see the official fee page.',page['url'])
  name=html.unescape(p.get('full_name') or p['name']).strip()
  alerts=[{'text':BeautifulText(x['message']),'url':x['url']} for x in p.get('notices',[])]
  stations.append({'id':p['idname'],'name':name+' — RV dump station','property_name':name,'operator':'Texas Parks and Wildlife Department','source_type':'state_park_agency','state':'Texas','state_code':'TX','city':loc['city'],'address':{'street':loc['address'],'city':loc['city'],'region':'TX','postal_code':loc['zip'],'country':'US','precision':'Park/property address, not the exact dump-station entrance.'},'last_checked':CHECKED,'verification_scope':'Official operator lists the dump-station amenity. Not an on-site inspection or confirmation that it is open today. One record per park, not per lane or physical outlet.','park_status':p['status'],'questions':facts,'alerts':alerts,'source_url':INDEX,'operator_url':p['url'],'sources':sources})
 # Specific access rules must never be generalized from other parks.
 restriction='https://tpwd.texas.gov/state-parks/lake-mineral-wells/fees-facilities/dump-station'
 for s in stations:
  if s['id']=='lake-mineral-wells':
   s['questions']['non_guest_access']=answer('Only wastewater generated at this park is accepted. Do not bring wastewater from elsewhere.',restriction)
   s['sources'].append({'url':restriction,'type':'state_park_agency','supports':['non_guest_access'],'evidence':'We can only accept wastewater generated at this park.','snapshot':'research/lake-mineral-wells-dump-rules.txt'})
  if s['id']=='lockhart':
   url='https://tpwd.texas.gov/state-parks/lockhart/fees-facilities/entrance-fees'
   # Only claim this when the fee page actually confirms day-use access.
   page=next((x for x in audits[s['id']]['pages'] if x['url']==url),{})
   if any('day use visitors' in t.lower() for t in page.get('dump_fee_blocks',[])):
    s['questions']['non_guest_access']=answer('Day-use visitors may use the dump station for its published fee plus daily entrance fee.',url)
 
 for extra in json.loads((ROOT/'research/additional-stations.json').read_text()):
  extra['questions']={k:answer() for k in QUESTIONS}
  stations.append(extra)
 data={'title':'RV Dump Stations USA','last_checked':CHECKED,'questions':QUESTIONS,'stations':stations}
 (ROOT/'data/stations.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
 print(f'Seeded {len(stations)} official-source properties')
def BeautifulText(value):
 from html.parser import HTMLParser
 class T(HTMLParser):
  def __init__(self):super().__init__();self.out=[]
  def handle_data(self,d):self.out.append(d)
 t=T();t.feed(html.unescape(value));return ' '.join(' '.join(t.out).split())
if __name__=='__main__':main()
