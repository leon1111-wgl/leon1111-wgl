#!/usr/bin/env python3
"""Check bilingual lessons, teaching scaffolds, stable anchors and sources."""
from pathlib import Path
from urllib.parse import urlparse
import json,re
ROOT=Path(__file__).resolve().parents[1]
KEYS=['title','story','concept','application','practice','symbols','calculation','limits','takeaway']

def validate_paths(require_all=True):
 errors=[];guides=[]
 def check(value,message):
  if not value:errors.append(message)
 def localized(value,label,allow_shared_term=False):
  valid=isinstance(value,dict) and set(value)=={'en','zh'} and all(value.values())
  check(valid,label+' needs complete EN/ZH values')
  if not valid:return
  en=' '.join(value['en']) if isinstance(value['en'],list) else value['en']
  zh=' '.join(value['zh']) if isinstance(value['zh'],list) else value['zh']
  check(not re.search('[\u4e00-\u9fff]',en),label+' has Chinese in English')
  check(bool(re.search('[\u4e00-\u9fff]',zh)) or (allow_shared_term and en==zh and len(zh)<=24),label+' has no Chinese translation')
 for name in ['ml','dl','vision','multimodal','start']:
  path=ROOT/'content'/('primer.json' if name=='start' else 'paths/'+name+'.json')
  if not path.exists():
   if require_all:errors.append('Missing bilingual guide '+name)
   continue
  g=json.loads(path.read_text());guides.append(g)
  size=8 if name=='start' else 16
  check(g['id']==name,name+' guide ID')
  check(len(g['topics'])==size and len(g['review'])==size,name+f' needs {size} topics/review cards')
  ids=[t['id'] for t in g['topics']]; mapped=[x for s in g['map'] for x in s['topics']]
  check(len(set(ids))==len(ids) and len(mapped)==len(set(mapped)) and set(ids)==set(mapped),name+' map coverage')
  if name!='start':check(len(g['map'])==4,name+' needs four learning stages')
  for s in g['map']:localized(s['title'],name+' map title')
  refs={r['id']:r for r in g['references']}
  check(len(refs)==len(g['references']) and len(refs)>=8,name+' references')
  for r in refs.values():
   check(urlparse(r['url']).scheme=='https' and bool(urlparse(r['url']).netloc),name+' invalid reference URL')
   localized(r['title'],name+' reference '+r['id'])
  for key in ['title','subtitle','description','coverage','prerequisites','outcomes']:localized(g[key],name+' '+key)
  for t in g['topics']:
   prefix=name+'/'+t['id']
   check(re.fullmatch('[a-z0-9-]+',t['id']) is not None,prefix+' invalid anchor')
   check(bool(t['formula'].strip()),prefix+' missing formula')
   check(t.get('level') in ['foundation','core','applied','advanced'],prefix+' learning level')
   check(bool(t['sources']) and set(t['sources'])<=set(refs),prefix+' missing source mapping')
   for key in KEYS:localized(t.get(key),prefix+'/'+key)
   for key,minimum,fields in [('glossary',3,['term','meaning']),('guided_questions',3,['question','answer']),('practice_cases',2,['title','body']),('code_examples',1,['title','intro','explanation'])]:
    entries=t.get(key,[])
    check(len(entries)>=minimum,prefix+' insufficient '+key)
    for i,entry in enumerate(entries):
     for field in fields:localized(entry.get(field),prefix+f'/{key}/{i}/{field}',allow_shared_term=(field=='term'))
   example_ids=[]
   for e in t.get('code_examples',[]):
    example_ids.append(e['id'])
    check(re.fullmatch('[a-z0-9-]+',e['id']) is not None,prefix+' unsafe example ID')
    check(bool(e.get('code','').strip()) and bool(e.get('output','').strip()),prefix+' missing code/output')
    try:compile(e['code'],prefix,'exec')
    except SyntaxError as ex:errors.append(prefix+' Python syntax: '+str(ex))
   check(len(example_ids)==len(set(example_ids)),prefix+' duplicate example ID')
  for r in g['review']:
   for key in ['title','body']:localized(r[key],name+' review '+key)
  for lang in ['en','zh']:
   page=ROOT/'site'/'ai'/f'{name}.{lang}.html'
   check(page.exists(),name+' missing rendered '+lang)
   if page.exists():
    text=page.read_text()
    for id in ids:check(f'id="{id}"' in text,name+' missing '+lang+' anchor '+id)
    check(f'data-language="{lang}" aria-current="page"' in text,name+' active language indicator')
    check(text.count('class="topic guide-topic"')==size,name+' topic rendering')
    check('Leon' in text,name+' branding absent')
    check('data-reading-size="large"' in text,name+' reading size control absent')
 profile=json.loads((ROOT/'content'/'profile.json').read_text())
 check(profile['github']=='https://github.com/leon1111-wgl','Incorrect GitHub destination')
 check(profile['education'][0]['degree']=='MSc','HKU qualification wording')
 for path in [ROOT/'README.md',ROOT/'profile'/'bio.txt',ROOT/'site'/'index.html',ROOT/'site'/'assets'/'profile-banner.svg']:
  check(not re.search(r'MSc (?:in )?Computer Science|study computer science at',path.read_text(),re.I),'Outdated degree wording '+path.name)
 return errors,guides
if __name__=='__main__':
 errors,guides=validate_paths()
 if errors:raise SystemExit('\n'.join(errors))
 print(f'PASS: {len(guides)} bilingual guides including the primer, {sum(len(g["topics"]) for g in guides)} translated topics, teaching scaffolds, source mappings and profile wording.')
