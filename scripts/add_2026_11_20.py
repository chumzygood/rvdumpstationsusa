"""Nov 20 2026: travel centers whose official, location-specific operator pages list an RV dump amenity
(Love's store pages: "RV Dump Service" in the Amenities list; TA page: "RV Dump" in Other Amenities). Pages were
captured by direct HTTPS request on 2026-11-20 and frozen as text in research/<id>-2026-11-20.txt; addresses come
from each page's own schema.org PostalAddress. Store hours and payment types are not assumed to apply to dumping.
Unknowns stay unknown."""
from pathlib import Path
import json,hashlib,re
ROOT=Path(__file__).resolve().parents[1]; D='2026-11-20'
SPEC=[
 ('loves-200','Love’s Travel Stop #200','Love’s Travel Stops','https://www.loves.com/locations/tx/amarillo/loves-travel-stop-amarillo-200','Amarillo','6930 I-40 E.','79120','RV Dump Service'),
 ('loves-231','Love’s Travel Stop #231','Love’s Travel Stops','https://www.loves.com/locations/tx/hillsboro/loves-travel-stop-hillsboro-231','Hillsboro','1501 Corsicana Hwy','76645','RV Dump Service'),
 ('loves-233','Love’s Travel Stop #233','Love’s Travel Stops','https://www.loves.com/locations/tx/waller/loves-travel-stop-waller-233','Waller','30710 FM 2920 Rd','77484','RV Dump Service'),
 ('loves-242','Love’s Travel Stop #242','Love’s Travel Stops','https://www.loves.com/locations/tx/san-antonio/loves-travel-stop-san-antonio-242','San Antonio','11361 S. I-35','78073','RV Dump Service'),
 ('loves-281','Love’s Travel Stop #281','Love’s Travel Stops','https://www.loves.com/locations/tx/fort-worth/loves-travel-stop-fort-worth-281','Fort Worth','200 Garden Acres Dr.','76140','RV Dump Service'),
 ('ta-terrell','TA Terrell #0233','TravelCenters of America','https://www.ta-petro.com/location/tx/ta-terrell/','Terrell','1700 Wilson Road','75161-5334','RV Dump'),
]
out=[]
for sid,pname,op,url,city,street,zip_,marker in SPEC:
  p=f'research/{sid}-2026-11-20.txt'; t=(ROOT/p).read_text(); sha=hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
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
(ROOT/'research/additional-stations-2026-11-20.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print('records',len(out))
