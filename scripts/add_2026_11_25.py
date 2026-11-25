"""Nov 25 2026: Love’s travel stops whose official, location-specific operator pages list an RV dump amenity
(Love's store pages: "RV Dump Service" in the Amenities list). Pages were
captured by direct HTTPS request on 2026-11-25 and frozen as text in research/<id>-2026-11-25.txt; addresses come
from each page's own schema.org PostalAddress. Store hours and payment types are not assumed to apply to dumping.
Unknowns stay unknown."""
from pathlib import Path
import json,hashlib,re
ROOT=Path(__file__).resolve().parents[1]; D='2026-11-25'
SPEC=[
 ('loves-623','Love’s Travel Stop #623','Love’s Travel Stops','https://www.loves.com/locations/tx/midland/loves-travel-stop-midland-623','Midland','5200 Cholla Rd','79706','RV Dump Service'),
 ('loves-852','Love’s Travel Stop #852','Love’s Travel Stops','https://www.loves.com/locations/tx/new-boston/loves-travel-stop-new-boston-852','New Boston','2486 US Hwy-82 W','75570','RV Dump Service'),
 ('loves-339','Love’s Travel Stop #339','Love’s Travel Stops','https://www.loves.com/locations/tx/odessa/loves-travel-stop-odessa-339','Odessa','1901 W. I-20','79766','RV Dump Service'),
 ('loves-492','Love’s Travel Stop #492','Love’s Travel Stops','https://www.loves.com/locations/tx/pecos/loves-travel-stop-pecos-492','Pecos','5202 South Cedar St.','79772','RV Dump Service'),
 ('loves-1049','Love’s Travel Stop #1049','Love’s Travel Stops','https://www.loves.com/locations/tx/premont/loves-travel-stop-premont-1049','Premont','511 NE 8th St','78375','RV Dump Service'),
 ('loves-283','Love’s Travel Stop #283','Love’s Travel Stops','https://www.loves.com/locations/tx/rockwall/loves-travel-stop-rockwall-283','Rockwall','1990 E. I-30','75075','RV Dump Service'),
 ('loves-960','Love’s Travel Stop #960','Love’s Travel Stops','https://www.loves.com/locations/tx/san-antonio/loves-travel-stop-san-antonio-960','San Antonio','9530 Southton Rd','78223','RV Dump Service'),
 ('loves-700','Love’s Travel Stop #700','Love’s Travel Stops','https://www.loves.com/locations/tx/sonora/loves-travel-stop-sonora-700','Sonora','3880 Loop 467','76950','RV Dump Service'),
]
out=[]
for sid,pname,op,url,city,street,zip_,marker in SPEC:
  p=f'research/{sid}-2026-11-25.txt'; t=(ROOT/p).read_text(); sha=hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
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
(ROOT/'research/additional-stations-2026-11-25.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print('records',len(out))
