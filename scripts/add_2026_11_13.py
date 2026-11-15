"""Nov 13 2026: federal campgrounds with a listed dump station from Recreation.gov (the federal reservation
system's own facility records), captured by direct HTTPS request to the public Recreation.gov campground
endpoint on 2026-11-13 (frozen in research/recgov-<id>.json). Unknowns stay unknown."""
from pathlib import Path
import json,hashlib,re,html
ROOT=Path(__file__).resolve().parents[1]; D='2026-11-13'
def clean(t): return ' '.join(re.sub(r'<[^>]+>',' ',html.unescape(t or '')).split())
def rec_for(eid):
  c=json.loads((ROOT/f'research/recgov-{eid}.json').read_text())['campground']; return c
def find(c,pat):
  texts=list((c.get('facility_description_map') or {}).values())+[n.get('notice_text','') for n in (c.get('notices') or [])]
  for t in texts:
    for sent in re.split(r'(?<=[.!?])\s+(?=[A-Z])',clean(t)):
      if re.search(pat,sent,re.I): return sent.strip()
  return None
SPEC=[
 # eid, id, property_name, operator, source_type, city, street, zip, precision
 ('234362','usfs-ratcliff-lake-recreation-area','Ratcliff Lake Recreation Area — Davy Crockett National Forest','USDA Forest Service','federal_usfs','Kennard','18551 State Highway 7 East','75487','Operator-listed facility address on Recreation.gov; verify the dump-station location inside the recreation area.'),
 ('232430','usfs-double-lake-recreation-area','Double Lake Recreation Area — Sam Houston National Forest','USDA Forest Service','federal_usfs','Coldspring','301 FM 2025','77331','Operator-listed facility address on Recreation.gov; verify the dump-station location inside the recreation area.'),
 ('233579','usace-patmayse-pat-mayse-west','Pat Mayse West Campground — Pat Mayse Lake','U.S. Army Corps of Engineers','federal_usace','Pat Mayse Lake area',None,None,None),
 ('233617','usace-patmayse-sanders-cove','Sanders Cove Campground — Pat Mayse Lake','U.S. Army Corps of Engineers','federal_usace','Pat Mayse Lake area',None,None,None),
 ('233527','usace-texoma-juniper-point','Juniper Point Campground — Lake Texoma','U.S. Army Corps of Engineers','federal_usace','Lake Texoma area',None,None,None),
 ('233595','usace-texoma-preston-bend','Preston Bend Campground — Lake Texoma','U.S. Army Corps of Engineers','federal_usace','Pottsboro','129 Preston Bend Park Road','75076','Operator-listed campground address on Recreation.gov; verify the dump-station entrance.'),
 ('234035','nps-big-bend-rio-grande-village','Rio Grande Village Campground — Big Bend National Park','National Park Service','federal_nps','Big Bend National Park area',None,None,None),
]
LAKE_PREC='Street address not confirmed (Recreation.gov lists only a mailing/office address). This is a named-area listing, not a precise-entrance claim; follow the official operator directions.'
out=[]
for eid,sid,pname,op,stype,city,street,zip_,prec in SPEC:
  c=rec_for(eid); url=f'https://www.recreation.gov/camping/campgrounds/{eid}'
  snap=f'research/recgov-{eid}.json'; sha=hashlib.sha256((ROOT/snap).read_bytes()).hexdigest()
  amen='Dump Station' in (c.get('amenities') or {})
  desc=find(c,r'dump station|fill/dump|dump/fill')
  ev=' '.join(x for x in [('Recreation.gov amenities list: “Dump Station”.' if amen else ''),(f'“{desc}”' if desc else '')] if x)
  assert 'dump' in ev.lower(),sid
  rec={'id':sid,'property_name':pname,'name':pname+' — RV dump station','operator':op,'source_type':stype,'state':'Texas','state_code':'TX','city':city,
       'address':{'street':street,'city':city,'region':'TX','postal_code':zip_,'country':'US','precision':prec or LAKE_PREC},'last_checked':D,
       'verification_scope':'The federal reservation system (Recreation.gov) lists the dump-station amenity for this campground. Not an on-site inspection or confirmation that it is open today. One record per property, not per lane or physical outlet.',
       'park_status':'Operating status not confirmed; check operator','alerts':[],'source_url':url,'operator_url':url,
       'sources':[{'url':url,'snapshot':snap,'sha256':sha,'capture_method':'Direct HTTPS request to the public Recreation.gov campground record (api/camps/campgrounds/'+eid+') on 2026-11-13.','type':stype,'supports':['dump_station','location'],'evidence':ev}],
       'question_overrides':{}}
  q=rec['question_overrides']
  def doc(k,ans): q[k]={'status':'documented','answer':ans,'source_url':url}
  def alert(t): rec['alerts'].append({'text':t,'url':url})
  gate=find(c,r'Entrance gate')
  if gate: alert(f'Recreation.gov: “{gate}” (gate hours, not confirmed dump-station hours).')
  if eid=='232430':
    fee=find(c,r'dump station use'); assert '$5 per use' in fee
    doc('fee',f'$5 per use for the dump station (Recreation.gov notice: “{fee}”).')
    late=find(c,r'No access from'); alert(f'Recreation.gov: “{late}” (camper arrival rule, not confirmed dump-station hours).')
  if eid=='234362':
    yr=find(c,r'Camping is available year-round'); assert yr
    doc('seasonal',f'Recreation.gov: “{yr}” (campground season; a separate dump-station season is not stated).')
    dayuse=find(c,r'Day-use fee'); alert(f'Recreation.gov: “{dayuse}” (day-use fee; a dump-station fee is not stated).')
  if eid in ('233579','233617'):
    yr=find(c,r'year-round campground'); assert yr
    doc('seasonal',f'Recreation.gov: “{yr}” (campground season; a separate dump-station season is not stated).')
  if eid=='233527':
    full=find(c,r'fully open from March 1'); east=find(c,r'Juniper East will be closed'); assert full and east
    doc('seasonal',f'Recreation.gov: “{full}” “{east}” (campground season; a separate dump-station season is not stated).')
    alert(f'Recreation.gov: “{east}” Starting Dec 1, 2026 parts of the park close for the off season; check which loop’s dump station is open.')
  if eid=='234035':
    hook=find(c,r'dump/fill station at the campground entrance')
    if hook: rec['sources'][0]['evidence']+=f' “{hook}”'
    ent=find(c,r'charges an entrance fee'); alert(f'Recreation.gov: “{ent}” (park entrance fee; a dump-station fee is not stated).')
  out.append(rec)
(ROOT/'research/additional-stations-2026-11-13.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print('records',len(out))
