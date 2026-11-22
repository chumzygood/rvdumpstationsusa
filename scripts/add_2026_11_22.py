"""Nov 22 2026: Love’s travel stops whose official, location-specific operator pages list an RV dump amenity
(Love's store pages: "RV Dump Service" in the Amenities list). Pages were
captured by direct HTTPS request on 2026-11-22 and frozen as text in research/<id>-2026-11-22.txt; addresses come
from each page's own schema.org PostalAddress. Store hours and payment types are not assumed to apply to dumping.
Unknowns stay unknown."""
from pathlib import Path
import json,hashlib,re
ROOT=Path(__file__).resolve().parents[1]; D='2026-11-22'
SPEC=[
 ('loves-615','Love’s Travel Stop #615','Love’s Travel Stops','https://www.loves.com/locations/tx/carthage/loves-travel-stop-carthage-615','Carthage','975 E Sabine St','75633','RV Dump Service'),
 ('loves-862','Love’s Travel Stop #862','Love’s Travel Stops','https://www.loves.com/locations/tx/cotulla/loves-travel-stop-cotulla-862','Cotulla','1963 S IH 35','78014','RV Dump Service'),
 ('loves-836','Love’s Travel Stop #836','Love’s Travel Stops','https://www.loves.com/locations/tx/dalhart/loves-travel-stop-dalhart-836','Dalhart','12182 Hwy 87 N','79022','RV Dump Service'),
 ('loves-294','Love’s Travel Stop #294','Love’s Travel Stops','https://www.loves.com/locations/tx/dallas/loves-travel-stop-dallas-294','Dallas','8800 S. Polk Street','75232','RV Dump Service'),
 ('loves-673','Love’s Travel Stop #673','Love’s Travel Stops','https://www.loves.com/locations/tx/domino/loves-travel-stop-domino-673','Domino','22406 US Highway 59 N','75572','RV Dump Service'),
 ('loves-739','Love’s Travel Stop #739','Love’s Travel Stops','https://www.loves.com/locations/tx/donna/loves-travel-stop-donna-739','Donna','545 W I-2','78537','RV Dump Service'),
 ('loves-297','Love’s Travel Stop #297','Love’s Travel Stops','https://www.loves.com/locations/tx/edna/loves-travel-stop-edna-297','Edna','1509 E. Rose St.','77957','RV Dump Service'),
]
out=[]
for sid,pname,op,url,city,street,zip_,marker in SPEC:
  p=f'research/{sid}-2026-11-22.txt'; t=(ROOT/p).read_text(); sha=hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
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
(ROOT/'research/additional-stations-2026-11-22.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print('records',len(out))
