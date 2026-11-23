"""Nov 23 2026: Love’s travel stops whose official, location-specific operator pages list an RV dump amenity
(Love's store pages: "RV Dump Service" in the Amenities list). Pages were
captured by direct HTTPS request on 2026-11-23 and frozen as text in research/<id>-2026-11-23.txt; addresses come
from each page's own schema.org PostalAddress. Store hours and payment types are not assumed to apply to dumping.
Unknowns stay unknown."""
from pathlib import Path
import json,hashlib,re
ROOT=Path(__file__).resolve().parents[1]; D='2026-11-23'
SPEC=[
 ('loves-288','Love’s Travel Stop #288','Love’s Travel Stops','https://www.loves.com/locations/tx/fairfield/loves-travel-stop-fairfield-288','Fairfield','299 I-45','75840','RV Dump Service'),
 ('loves-542','Love’s Travel Stop #542','Love’s Travel Stops','https://www.loves.com/locations/tx/fort-stockton/loves-travel-stop-fort-stockton-542','Fort Stockton','2723 East US Highway 290','79735','RV Dump Service'),
 ('loves-885','Love’s Travel Stop #885','Love’s Travel Stops','https://www.loves.com/locations/tx/harlingen/loves-travel-stop-harlingen-885','Harlingen','21379 US 77 Expressway','78550','RV Dump Service'),
 ('loves-375','Love’s Travel Stop #375','Love’s Travel Stops','https://www.loves.com/locations/tx/hearne/loves-travel-stop-hearne-375','Hearne','1423 N Market St','77859','RV Dump Service'),
 ('loves-642','Love’s Travel Stop #642','Love’s Travel Stops','https://www.loves.com/locations/tx/hereford/loves-travel-stop-hereford-642','Hereford','901 West 1st St','79045','RV Dump Service'),
 ('loves-315','Love’s Travel Stop #315','Love’s Travel Stops','https://www.loves.com/locations/tx/houston/loves-travel-stop-houston-315','Houston','3940 N McCarty St','77013','RV Dump Service'),
 ('loves-617','Love’s Travel Stop #617','Love’s Travel Stops','https://www.loves.com/locations/tx/hungerford/loves-travel-stop-hungerford-617','Hungerford','350 E Walnut Street','77448','RV Dump Service'),
 ('loves-331','Love’s Travel Stop #331','Love’s Travel Stops','https://www.loves.com/locations/tx/hutchins/loves-travel-stop-hutchins-331','Hutchins','2500 S. I-45','75141','RV Dump Service'),
]
out=[]
for sid,pname,op,url,city,street,zip_,marker in SPEC:
  p=f'research/{sid}-2026-11-23.txt'; t=(ROOT/p).read_text(); sha=hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
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
(ROOT/'research/additional-stations-2026-11-23.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print('records',len(out))
