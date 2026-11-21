"""Nov 21 2026: Love’s travel stops whose official, location-specific operator pages list an RV dump amenity
(Love's store pages: "RV Dump Service" in the Amenities list). Pages were
captured by direct HTTPS request on 2026-11-21 and frozen as text in research/<id>-2026-11-21.txt; addresses come
from each page's own schema.org PostalAddress. Store hours and payment types are not assumed to apply to dumping.
Unknowns stay unknown."""
from pathlib import Path
import json,hashlib,re
ROOT=Path(__file__).resolve().parents[1]; D='2026-11-21'
SPEC=[
 ('loves-721','Love’s Travel Stop #721','Love’s Travel Stops','https://www.loves.com/locations/tx/alma/loves-travel-stop-alma-721','Alma','6550 S Interstate 45 Service Rd','75119','RV Dump Service'),
 ('loves-250','Love’s Travel Stop #250','Love’s Travel Stops','https://www.loves.com/locations/tx/amarillo/loves-travel-stop-amarillo-250','Amarillo','14701 I-40 W.','79124','RV Dump Service'),
 ('loves-539','Love’s Travel Stop #539','Love’s Travel Stops','https://www.loves.com/locations/tx/andrews/loves-travel-stop-andrews-539','Andrews','1201 S. Main St.','79714','RV Dump Service'),
 ('loves-299','Love’s Travel Stop #299','Love’s Travel Stops','https://www.loves.com/locations/tx/anna/loves-travel-stop-anna-299','Anna','1701 US Highway 75','75409','RV Dump Service'),
 ('loves-696','Love’s Travel Stop #696','Love’s Travel Stops','https://www.loves.com/locations/tx/beaumont/loves-travel-stop-beaumont-696','Beaumont','7495 Smith Rd','77713','RV Dump Service'),
 ('loves-976','Love’s Travel Stop #976','Love’s Travel Stops','https://www.loves.com/locations/tx/big-spring/loves-travel-stop-big-spring-976','Big Spring','1801 W I-20','79720','RV Dump Service'),
 ('loves-713','Love’s Travel Stop #713','Love’s Travel Stops','https://www.loves.com/locations/tx/bridgeport/loves-travel-stop-bridgeport-713','Bridgeport','2300 US Highway 380','76426','RV Dump Service'),
 ('loves-767','Love’s Travel Stop #767','Love’s Travel Stops','https://www.loves.com/locations/tx/brownsville/loves-travel-stop-brownsville-767','Brownsville','3400 Nafta Parkway','78526','RV Dump Service'),
]
out=[]
for sid,pname,op,url,city,street,zip_,marker in SPEC:
  p=f'research/{sid}-2026-11-21.txt'; t=(ROOT/p).read_text(); sha=hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
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
(ROOT/'research/additional-stations-2026-11-21.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print('records',len(out))
