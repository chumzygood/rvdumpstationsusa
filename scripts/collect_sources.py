"""Refresh official TPWD source snapshots. Never run implicitly during builds."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import requests,json,hashlib
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
INDEX='https://tpwd.texas.gov/state-parks/parks-map'
def fetch(url,key):
    r=requests.get(url,timeout=35);r.raise_for_status()
    s=BeautifulSoup(r.text,'html.parser')
    for t in s(['script','style']):t.decompose()
    text=s.get_text(' ',strip=True)
    (ROOT/'research'/f'{key}.txt').write_text(text)
    return s,text

def one(p):
    slug=p['idname'];result={'slug':slug,'pages':[]}
    for suffix,key in [('', 'home'),('/fees-facilities/campsites','camping'),('/fees-facilities/entrance-fees','fees')]:
        url=p['url']+suffix
        try:
            soup,text=fetch(url,f'{slug}-{key}')
            fees=[]
            for h in soup.select('h2,h3,h4'):
                if 'dump station fee' in h.get_text(' ',strip=True).lower():
                    fees.append((h.find_parent(class_='chartrow') or h.parent).get_text(' ',strip=True))
            main=soup.select_one('#content-core') or soup.select_one('main') or soup
            snippets=[]
            for t in main.find_all(string=lambda t:t and ('dump station' in t.lower() or 'dump-station' in t.lower())):
                v=t.parent.get_text(' ',strip=True)
                if len(v)<1800 and v not in snippets:snippets.append(v)
            result['pages'].append({'url':url,'snapshot':f'research/{slug}-{key}.txt','sha256':hashlib.sha256(text.encode()).hexdigest(),'dump_fee_blocks':fees,'dump_mentions':snippets})
        except Exception as e:result['pages'].append({'url':url,'error':str(e)})
    print(slug,flush=True)
    return result
if __name__=='__main__':
    r=requests.get(INDEX,timeout=35);r.raise_for_status()
    (ROOT/'research/texas-directory.html').write_text(r.text)
    parks=json.JSONDecoder().raw_decode(r.text.split('var jsonResults=')[1])[0]
    (ROOT/'research/texas-official.json').write_text(json.dumps(parks,indent=2))
    candidates=[p for p in parks if 'dump_station' in p['amenities'] and p['status']!='Closed' and p['idname']!='barton-warnock']
    results=list(ThreadPoolExecutor(max_workers=4).map(one,candidates))
    (ROOT/'research/source-audit.json').write_text(json.dumps(results,indent=2))
    print('Completed',len(results),'locations')
