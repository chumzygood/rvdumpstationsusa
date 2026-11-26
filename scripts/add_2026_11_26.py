"""Nov 26 2026: Love’s travel stops whose official, location-specific operator pages list an RV dump amenity
(Love's store pages: "RV Dump Service" in the Amenities list). Pages were
captured by direct HTTPS request on 2026-11-26 and frozen as text in research/<id>-2026-11-26.txt; addresses come
from each page's own schema.org PostalAddress. Store hours and payment types are not assumed to apply to dumping.
Unknowns stay unknown."""
from pathlib import Path
import json,hashlib,re
ROOT=Path(__file__).resolve().parents[1]; D='2026-11-26'
SPEC=[
 ('loves-287','Love’s Travel Stop #287','Love’s Travel Stops','https://www.loves.com/locations/tx/van/loves-travel-stop-van-287','Van','1221 S. Oak St','75790','RV Dump Service'),
 ('loves-651','Love’s Travel Stop #651','Love’s Travel Stops','https://www.loves.com/locations/tx/van/loves-travel-stop-van-651','Van','1188 S. Oak St.','75790','RV Dump Service'),
 ('loves-738','Love’s Travel Stop #738','Love’s Travel Stops','https://www.loves.com/locations/tx/sulphur-springs/loves-travel-stop-sulphur-springs-738','Sulphur Springs','1201 S Hillcrest Dr','75482','RV Dump Service'),
 ('loves-719','Love’s Travel Stop #719','Love’s Travel Stops','https://www.loves.com/locations/tx/troy/loves-travel-stop-troy-719','Troy','1610 Cotton Gin Rd','76579','RV Dump Service'),
 ('loves-984','Love’s Travel Stop #984','Love’s Travel Stops','https://www.loves.com/locations/tx/tulia/loves-travel-stop-tulia-984','Tulia','2851 W TX-86','79088','RV Dump Service'),
 ('loves-484','Love’s Travel Stop #484','Love’s Travel Stops','https://www.loves.com/locations/tx/weimar/loves-travel-stop-weimar-484','Weimar','900 S Eagle Street','78962','RV Dump Service'),
 ('loves-468','Love’s Travel Stop #468','Love’s Travel Stops','https://www.loves.com/locations/tx/willis/loves-travel-stop-willis-468','Willis','9600 Longstreet Rd','77318','RV Dump Service'),
 ('loves-815','Love’s Travel Stop #815','Love’s Travel Stops','https://www.loves.com/locations/tx/winona/loves-travel-stop-winona-815','Winona','12577 CR 3101','75792','RV Dump Service'),
]
out=[]
for sid,pname,op,url,city,street,zip_,marker in SPEC:
  p=f'research/{sid}-2026-11-26.txt'; t=(ROOT/p).read_text(); sha=hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
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
(ROOT/'research/additional-stations-2026-11-26.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print('records',len(out))
