"""Offline public-site acceptance: sources, routes, metadata, sitemap, determinism."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse,unquote
from xml.etree import ElementTree as ET
import json,subprocess,hashlib
R=Path(__file__).resolve().parents[1];OUT=R/'docs';DOMAIN='https://rvdumpstationsusa.com'
D=json.loads((R/'data/stations.json').read_text());S=D['stations']
assert len(S)>=50 and len({s['id'] for s in S})==len(S)
parks={p['idname']:p for p in json.loads((R/'research/texas-official.json').read_text())}
hosts={'tpwd.texas.gov','www.swf-wc.usace.army.mil','www.loves.com','www.ta-petro.com','pilotcompany.com'}
for s in S:
 assert s['last_checked']=='2026-11-10'
 assert s['source_type'] in ['state_park_agency','federal_usace','travel_center_operator']
 if s['source_type']=='state_park_agency':
  assert 'dump_station' in parks[s['id']]['amenities']
  assert s['address']['street']==parks[s['id']]['location']['address']
 else:assert any('dump' in v.get('evidence','').lower() for v in s['sources'])
 assert set(s['questions'])==set(D['questions'])
 urls={v['url'] for v in s['sources']}
 for k,a in s['questions'].items():
  assert a['status'] in ['unknown','documented']
  assert (a['source_url'] in urls) if a['status']=='documented' else a['source_url'] is None
 for v in s['sources']:
  assert urlparse(v['url']).hostname in hosts
  assert (R/v['snapshot']).exists()
  if 'sha256' in v:assert hashlib.sha256((R/v['snapshot']).read_bytes()).hexdigest()==v['sha256']
assert '$10' in next(s for s in S if s['id']=='lockhart')['questions']['fee']['answer']
assert 'April 1, 2027' in ' '.join(x['text'] for x in next(s for s in S if s['id']=='seminole-canyon')['alerts'])
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.robots=None;self.canonical=None;self.schema=[];self.injson=False
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag in ['a','link'] and 'href' in a:self.links.append(a['href'])
  if tag=='meta' and a.get('name')=='robots':self.robots=a.get('content')
  if tag=='link' and a.get('rel')=='canonical':self.canonical=a['href']
  if tag=='script' and a.get('type')=='application/ld+json':self.injson=True
 def handle_data(self,data):
  if self.injson:self.schema.append(json.loads(data))
 def handle_endtag(self,tag):
  if tag=='script':self.injson=False
canonicals=set()
for f in OUT.rglob('*.html'):
 p=Parser();p.feed(f.read_text());is404=f.name=='404.html'
 assert p.robots==('noindex,follow' if is404 else 'index,follow'),f
 assert p.canonical and p.canonical.startswith(DOMAIN+'/')
 if not is404:assert p.canonical not in canonicals;canonicals.add(p.canonical)
 assert p.schema,f
 for u in p.links:
  if urlparse(u).scheme or u.startswith('#'):continue
  q=OUT/unquote(u).lstrip('/')
  if u.endswith('/'):q=q/'index.html'
  assert q.exists(),(f,u)
 if 'stations' in f.parts:assert any(x.get('@type')=='Place' and x.get('url')==p.canonical for x in p.schema)
 assert 'https://tossmap.com/' in f.read_text()
site=ET.parse(OUT/'sitemap.xml');locs={x.text for x in site.findall('.//{*}loc')}
assert locs==canonicals and len(locs)==len(canonicals)
assert (OUT/'CNAME').read_text().strip()=='rvdumpstationsusa.com'
assert 'Disallow: /' not in (OUT/'robots.txt').read_text()
assert DOMAIN+'/sitemap.xml' in (OUT/'robots.txt').read_text()
assert not (OUT/'states').exists() and not (OUT/'cities').exists() and not (OUT/'stations').exists()
assert 'coming soon' in (OUT/'index.html').read_text() and not (OUT/'florida').exists()
before={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.rglob('*') if p.is_file()}
subprocess.run(['python3',str(R/'scripts/build.py')],check=True,capture_output=True)
after={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.rglob('*') if p.is_file()}
assert before==after,'Build not deterministic'
print(f'PASS: {len(S)} official-source properties, {len(canonicals)+1} HTML pages; evidence hashes, field provenance, internal links, canonical/schema URLs, sitemap coverage, robots, CNAME, route migration and deterministic build.')
