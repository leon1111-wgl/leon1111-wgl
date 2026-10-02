#!/usr/bin/env python3
"""Check bilingual coverage, stable anchors, source mapping and publication wording."""
from pathlib import Path
from urllib.parse import urlparse
import json,re
ROOT=Path(__file__).resolve().parents[1]
KEYS=['title','story','concept','application','practice','symbols','calculation','limits','takeaway']
RANGES={'story':(110,170),'concept':(70,120),'application':(50,90),'practice':(50,90),'symbols':(70,110),'calculation':(100,160),'limits':(35,70),'takeaway':(15,35)}
def validate_paths(require_all=True):
 errors=[];guides=[]
 def check(value,message):
  if not value:errors.append(message)
 for name in ['ml','dl','vision','multimodal']:
  path=ROOT/'content'/'paths'/(name+'.json')
  if not path.exists():
   if require_all:errors.append('Missing bilingual guide '+name)
   continue
  g=json.loads(path.read_text());guides.append(g)
  check(g['id']==name,name+' guide ID')
  check(len(g['topics'])==8 and len(g['review'])==8,name+' needs eight topics/review cards')
  ids=[t['id'] for t in g['topics']]; mapped=[x for s in g['map'] for x in s['topics']]
  check(len(set(ids))==len(ids) and len(mapped)==len(set(mapped)) and set(ids)==set(mapped),name+' map coverage')
  refs={r['id']:r for r in g['references']}
  check(len(refs)==len(g['references']) and len(refs)>=8,name+' references')
  for r in refs.values():check(urlparse(r['url']).scheme=='https' and bool(urlparse(r['url']).netloc),name+' invalid reference URL')
  for key in ['title','subtitle','description','coverage','prerequisites','outcomes']:
   check(all(g[key].get(l) for l in ['en','zh']),name+' localized '+key)
  for t in g['topics']:
   prefix=name+'/'+t['id']
   check(re.fullmatch('[a-z0-9-]+',t['id']) is not None,prefix+' invalid anchor')
   check(bool(t['formula'].strip()),prefix+' missing formula')
   check(bool(t['sources']) and set(t['sources'])<=set(refs),prefix+' missing source mapping')
   for key in KEYS:
    check(set(t[key])=={'en','zh'} and all(t[key].values()),prefix+' missing translation '+key)
    check(not re.search('[\u4e00-\u9fff]',t[key]['en']),prefix+' Chinese in English field '+key)
    check(bool(re.search('[\u4e00-\u9fff]',t[key]['zh'])),prefix+' Chinese translation absent '+key)
    if key in RANGES:
     count=len(re.findall(r"\S+",t[key]['en']));lo,hi=RANGES[key]
     check(lo<=count<=hi,prefix+' '+key+f' has {count} words; target {lo}-{hi}')
  for lang in ['en','zh']:
   page=ROOT/'site'/'ai'/f'{name}.{lang}.html'
   check(page.exists(),name+' missing rendered '+lang)
   if page.exists():
    text=page.read_text()
    for id in ids:check(f'id="{id}"' in text,name+' missing '+lang+' anchor '+id)
    check(f'data-language="{lang}" aria-current="page"' in text,name+' active language indicator')
    check(len(re.findall('class="topic guide-topic"',text))==8,name+' topic rendering')
    check('Guoliang' in text,name+' branding absent')
 profile=json.loads((ROOT/'content'/'profile.json').read_text())
 check(profile['github']=='https://github.com/leon1111-wgl','Incorrect GitHub destination')
 check(profile['education'][0]['degree']=='MSc','HKU qualification wording')
 for path in [ROOT/'README.md',ROOT/'profile'/'bio.txt',ROOT/'site'/'index.html',ROOT/'site'/'assets'/'profile-banner.svg']:
  check(not re.search(r'MSc (?:in )?Computer Science|study computer science at',path.read_text(),re.I),'Outdated degree wording '+path.name)
 return errors,guides
if __name__=='__main__':
 errors,guides=validate_paths()
 if errors:raise SystemExit('\n'.join(errors))
 print(f'PASS: {len(guides)} bilingual guides, {sum(len(g["topics"]) for g in guides)} translated topics, source mappings, reading anchors and profile wording.')
