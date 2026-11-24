"""Nov 24 2026: Love’s travel stops whose official, location-specific operator pages list an RV dump amenity
(Love's store pages: "RV Dump Service" in the Amenities list). Pages were
captured by direct HTTPS request on 2026-11-24 and frozen as text in research/<id>-2026-11-24.txt; addresses come
from each page's own schema.org PostalAddress. Store hours and payment types are not assumed to apply to dumping.
Unknowns stay unknown."""
from pathlib import Path
import json,hashlib,re
ROOT=Path(__file__).resolve().parents[1]; D='2026-11-24'
SPEC=[
 ('loves-628','Love’s Travel Stop #628','Love’s Travel Stops','https://www.loves.com/locations/tx/italy/loves-travel-stop-italy-628','Italy','1021 Dale Evans Dr','76651','RV Dump Service'),
 ('loves-234','Love’s Travel Stop #234','Love’s Travel Stops','https://www.loves.com/locations/tx/katy/loves-travel-stop-katy-234','Katy','612 Pederson Rd.','77494','RV Dump Service'),
 ('loves-853','Love’s Travel Stop #853','Love’s Travel Stops','https://www.loves.com/locations/tx/kermit/loves-travel-stop-kermit-853','Kermit','674 E State Hwy 302','79745','RV Dump Service'),
 ('loves-327','Love’s Travel Stop #327','Love’s Travel Stops','https://www.loves.com/locations/tx/kingsville/loves-travel-stop-kingsville-327','Kingsville','1451 N US Highway 77 Byp','78363','RV Dump Service'),
 ('loves-762','Love’s Travel Stop #762','Love’s Travel Stops','https://www.loves.com/locations/tx/laredo/loves-travel-stop-laredo-762','Laredo','101 Pinnacle Road','78045','RV Dump Service'),
 ('loves-589','Love’s Travel Stop #589','Love’s Travel Stops','https://www.loves.com/locations/tx/lubbock/loves-travel-stop-lubbock-589','Lubbock','4221 North Interstate 27','79403','RV Dump Service'),
 ('loves-290','Love’s Travel Stop #290','Love’s Travel Stops','https://www.loves.com/locations/tx/lufkin/loves-travel-stop-lufkin-290','Lufkin','1003 S. Medford Dr.','75901','RV Dump Service'),
 ('loves-709','Love’s Travel Stop #709','Love’s Travel Stops','https://www.loves.com/locations/tx/lufkin/loves-travel-stop-lufkin-709','Lufkin','5614 Hwy 59 N','75901','RV Dump Service'),
]
out=[]
for sid,pname,op,url,city,street,zip_,marker in SPEC:
  p=f'research/{sid}-2026-11-24.txt'; t=(ROOT/p).read_text(); sha=hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
  assert marker in t and street.split()[0] in t and city in t,sid
  if sid.startswith('loves'):
    am=re.search(r'Amenities (.*?) Hide Learn More',t); assert am and 'RV Dump Service' in am.group(1),sid
    ev='Location-specific amenities list: RV Dump Service. Store hours and general payment types are not assumed to apply to dumping.'
  else:
    am=re.search(r'Other Amenities (.*?) Recent Blog Posts',t); assert am and 'RV Dump' in am.group(1),sid
    ev='Location amenities include RV Dump.'
  rec={'id':sid,'property_name':pname,'name':pname+' — RV dump station','operator':op,'source_type':'travel_center_operator','state':'Texas','state_code':'TX','city':city,
       'address':{'street':street,'city':city,'region':'TX','postal_code':zip_,'country':'US','precision':'Operator property address; verify the dump-station entrance.'},'last_checked':D,
       'verification_scope':'Official operator lists the dump-station amenity. Not an on-site inspection or confirmation that it is open today. One record per property, not per lane or physical outlet.',
       'park_status':'Operating status not confirmed; check operator','alerts':[],'source_url':url,'operator_url':url,
       'sources':[{'url':url,'snapshot':p,'sha256':sha,'capture_method':f'Direct HTTPS request to the public operator location page on {D}; visible text frozen.','type':'travel_center_operator','supports':['dump_station','location'],'evidence':ev}],
       'question_overrides':{}}
  out.append(rec)
(ROOT/'research/additional-stations-2026-11-24.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print('records',len(out))
