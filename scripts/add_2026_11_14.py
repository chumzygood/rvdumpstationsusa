"""Nov 14 2026: federal campgrounds with a listed dump station from Recreation.gov (the federal reservation
system's own facility records), captured by direct HTTPS request to the public Recreation.gov campground
endpoint on 2026-11-14 (frozen in research/recgov-<id>.json). Unknowns stay unknown."""
from pathlib import Path
import json,hashlib,re,html
ROOT=Path(__file__).resolve().parents[1]; D='2026-11-14'
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
 ('232695','usace-somerville-rocky-creek','Rocky Creek Park — Somerville Lake','U.S. Army Corps of Engineers','federal_usace','Somerville Lake area',None,None,None),
 ('232607','usace-benbrook-holiday-park','Holiday Park — Benbrook Lake','U.S. Army Corps of Engineers','federal_usace','Benbrook Lake area',None,None,None),
 ('232557','usace-proctor-copperas-creek','Copperas Creek Park — Proctor Lake','U.S. Army Corps of Engineers','federal_usace','Proctor Lake area',None,None,None),
 ('232534','usace-lakeopines-brushy-creek','Brushy Creek Park — Lake O\' the Pines','U.S. Army Corps of Engineers','federal_usace','Lake O\' the Pines area',None,None,None),
 ('232636','usace-steinhagen-magnolia-ridge','Magnolia Ridge Park — B. A. Steinhagen Lake','U.S. Army Corps of Engineers','federal_usace','Steinhagen Lake area',None,None,None),
 ('232685','usace-samrayburn-rayburn-park','Rayburn Park — Sam Rayburn Reservoir','U.S. Army Corps of Engineers','federal_usace','Sam Rayburn Reservoir area',None,None,None),
 ('232583','usace-lavon-east-fork','East Fork Park — Lavon Lake','U.S. Army Corps of Engineers','federal_usace','Lavon Lake area',None,None,None),
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
       'sources':[{'url':url,'snapshot':snap,'sha256':sha,'capture_method':'Direct HTTPS request to the public Recreation.gov campground record (api/camps/campgrounds/'+eid+') on 2026-11-14.','type':stype,'supports':['dump_station','location'],'evidence':ev}],
       'question_overrides':{}}
  q=rec['question_overrides']
  def doc(k,ans): q[k]={'status':'documented','answer':ans,'source_url':url}
  def alert(t): rec['alerts'].append({'text':t,'url':url})
  gate=find(c,r'Entrance gate')
  if gate: alert(f'Recreation.gov: “{gate}” (gate hours, not confirmed dump-station hours).')
  for e_,pat in [('232607',r'main park for individual and family camping year-round'),('232636',r'year-round campground'),('232685',r'open year-round')]:
    if eid==e_:
      yr=find(c,pat); assert yr,eid
      doc('seasonal',f'Recreation.gov: “{yr}” (campground season; a separate dump-station season is not stated).')
  if eid=='232636':
    ns=find(c,r'NO sewer hook-ups'); assert ns
    rec['sources'][0]['evidence']+=f' “{ns}”'
  if eid=='232583':
    ent=find(c,r'dump station located near the park entrance'); assert ent
  out.append(rec)
(ROOT/'research/additional-stations-2026-11-14.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print('records',len(out))
