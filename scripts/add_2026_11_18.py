"""Nov 18 2026: National Park Service units in Texas whose official nps.gov camping pages state an RV dump
station. Pages were captured by direct HTTPS request on 2026-11-18 and frozen as text in
research/nps-<unit>-camping-2026-11-18.txt. Unknowns stay unknown."""
from pathlib import Path
import json,hashlib,re
ROOT=Path(__file__).resolve().parents[1]; D='2026-11-18'
def snap(unit):
  p=f'research/nps-{unit}-camping-2026-11-18.txt'; t=(ROOT/p).read_text()
  return p,t,hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def sent(t,pat):
  for line in t.splitlines():
    for s in re.split(r'(?<=[.!?])\s+(?=[A-Z])',' '.join(line.split())):
      if re.search(pat,s,re.I): return s.strip()
  raise AssertionError(pat)
PREC='Street address not confirmed (the official page names the location but gives no street address). This is a named-area listing, not a precise-entrance claim; follow the official operator directions.'
SPEC=[
 ('amis','https://www.nps.gov/amis/planyourvisit/camping.htm','nps-amistad-diablo-east','Diablo East area — Amistad National Recreation Area','Amistad NRA area',r'RV dump station with potable water is available'),
 ('lamr','https://www.nps.gov/lamr/planyourvisit/camping.htm','nps-lake-meredith-fritch-fortress','Fritch Fortress Campground — Lake Meredith National Recreation Area','Lake Meredith area',r'Dump stations with non-potable water are located near Fritch Fortress'),
 ('lamr','https://www.nps.gov/lamr/planyourvisit/camping.htm','nps-lake-meredith-sanford-yake','Sanford-Yake Campground — Lake Meredith National Recreation Area','Lake Meredith area',r'Dump stations with non-potable water are located near Fritch Fortress and Sanford-Yake'),
 ('pais','https://www.nps.gov/pais/planyourvisit/camping.htm','nps-padre-island-malaquite','Malaquite Campground — Padre Island National Seashore','Padre Island National Seashore area',r'RV dump station and freshwater filling station is located next to the entrance of Malaquite'),
]
out=[]
for unit,url,sid,pname,city,pat in SPEC:
  p,t,sha=snap(unit); ev=f'“{sent(t,pat)}”'
  extra=[]
  if unit=='amis': extra=[f'“{sent(t,r"It is located along the road to the Diablo East boat ramp")}”']
  if unit=='pais': extra=[f'“{sent(t,r"It is available for all park visitors to use")}”']
  rec={'id':sid,'property_name':pname,'name':pname+' — RV dump station','operator':'National Park Service','source_type':'federal_nps','state':'Texas','state_code':'TX','city':city,
       'address':{'street':None,'city':city,'region':'TX','postal_code':None,'country':'US','precision':PREC},'last_checked':D,
       'verification_scope':'The official National Park Service camping page states the dump station. Not an on-site inspection or confirmation that it is open today. One record per property, not per lane or physical outlet.',
       'park_status':'Operating status not confirmed; check operator','alerts':[],'source_url':url,'operator_url':url,
       'sources':[{'url':url,'snapshot':p,'sha256':sha,'capture_method':f'Direct HTTPS request to the public nps.gov camping page on {D}; visible text frozen.','type':'federal_nps','supports':['dump_station','location'],'evidence':' '.join([ev]+extra)}],
       'question_overrides':{}}
  q=rec['question_overrides']
  def doc(k,ans): q[k]={'status':'documented','answer':ans,'source_url':url}
  if unit=='amis':
    doc('potable_water','NPS: “An RV dump station with potable water is available…”')
    doc('non_guest_access','No. NPS: available “only to those with receipts showing they are camping within Amistad National Recreation Area campgrounds.”')
  if unit=='lamr':
    doc('potable_water','No drinking water at the dump station. NPS: “Dump stations with non-potable water are located near Fritch Fortress and Sanford-Yake campgrounds.”')
  if unit=='pais':
    doc('potable_water','NPS: “An RV dump station and freshwater filling station is located next to the entrance of Malaquite Campground.”')
    doc('non_guest_access','Yes. NPS: “It is available for all park visitors to use.” Park entrance fees apply.')
    rec['alerts'].append({'text':'NPS: “Park entrance fees are required.” (park entrance fee; a separate dump-station fee is not stated).','url':url})
  out.append(rec)
(ROOT/'research/additional-stations-2026-11-18.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print('records',len(out))
