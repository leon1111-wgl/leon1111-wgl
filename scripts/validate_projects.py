"""Validate bilingual project teaching, source identity and archive completeness."""
from pathlib import Path
from html.parser import HTMLParser
from zipfile import ZipFile
import json,re
from build_projects import projects,source,file_id
ROOT=Path(__file__).resolve().parents[1];SITE=ROOT/'site'
class Blocks(HTMLParser):
 def __init__(self):super().__init__();self.blocks={};self.active=None
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='code' and a.get('id','').startswith(('code-file-','project-snippet-')):self.active=a['id'];self.blocks[self.active]=''
 def handle_endtag(self,tag):
  if tag=='code':self.active=None
 def handle_data(self,data):
  if self.active:self.blocks[self.active]+=data

def validate_projects():
 errors=[];counts={'projects':0,'files':0,'milestones':0};ps=projects();combined={}
 def check(ok,msg):
  if not ok:errors.append(msg)
 def bilingual(value,label):
  if isinstance(value,dict):
   if 'en' in value or 'zh' in value:
    check(set(value)=={'en','zh'} and all(isinstance(x,str) and x.strip() for x in value.values()),label+': incomplete bilingual field')
    check(bool(re.search('[\u4e00-\u9fff]',value.get('zh',''))),label+': untranslated Chinese field')
   else:
    for k,v in value.items():bilingual(v,label+'/'+k)
  elif isinstance(value,list):
   for i,v in enumerate(value):bilingual(v,label+'/'+str(i))
 check({p['id'] for p in ps}=={'comp2017-log-analyzer','comp2017-process-runner','comp2017-thread-pipeline'},'Expected three complete COMP2017 workshops')
 topics={t['id'] for t in json.loads((ROOT/'content/COMP2017.json').read_text())['topics']}
 for p in ps:
  id=p['id'];bilingual(p,id);counts['projects']+=1
  for k,n in [('requirements',4),('milestones',4),('runs',3),('debugging',4),('test_plan',6),('design_notes',3),('extensions',2),('files',5)]:check(len(p.get(k,[]))>=n,id+': insufficient '+k)
  check(all(x['topic'] in topics for x in p['prerequisites']),id+': invalid prerequisite topic')
  check(len({m['id'] for m in p['milestones']})==len(p['milestones']),id+': duplicate milestone IDs')
  for m in p['milestones']:check(len(m['steps'])>=3 and m['snippet']['code'].strip(),id+': incomplete milestone')
  check(len(p['architecture']['ownership'])>=3 and len(p['architecture']['nodes'])>=3,id+': incomplete architecture')
  names=[f['path'] for f in p['files']]
  check(len(names)==len(set(names)),id+': duplicate source path')
  check(len({f['read_order'] for f in p['files']})==len(names),id+': duplicate reading order')
  actual={str(f.relative_to(ROOT/'projects'/id)) for f in (ROOT/'projects'/id).rglob('*') if f.is_file()}
  check(actual==set(names),id+': unlisted or missing files '+str(actual.symmetric_difference(set(names))))
  expected={};entries={}
  for f in p['files']:
   raw=(ROOT/'projects'/id/f['path']).read_bytes();text=raw.decode('utf-8');check(len(f['walkthrough'])>=3,id+'/'+f['path']+': incomplete walkthrough')
   check((SITE/'project-code'/id/f['path']).read_bytes()==raw,id+': exported source mismatch')
   expected['code-'+file_id(f['path'])]=text.removesuffix('\n');entries[id+'/'+f['path']]=raw
  expected.update({'project-snippet-'+m['id']:m['snippet']['code'].removesuffix('\n') for m in p['milestones']})
  for lang in ['en','zh']:
   page=SITE/'projects'/f'{id}.{lang}.html';parser=Blocks();parser.feed(page.read_text())
   check({k:v.removesuffix('\n') for k,v in parser.blocks.items()}==expected,id+'/'+lang+': rendered source differs')
   check('class="learning-route"' in page.read_text(),id+': missing opening route')
   check('assets/maps/' in (SITE/'notes'/f'{id}.{lang}.md').read_text()[:1200],id+': missing Markdown route')
  with ZipFile(SITE/'downloads'/f'{id}.zip') as z:
   check(z.testzip() is None and set(z.namelist())==set(entries),id+': archive membership mismatch')
   for name,data in entries.items():check(z.read(name)==data,id+': archive source mismatch '+name)
  combined.update(entries);counts['files']+=len(names);counts['milestones']+=len(p['milestones'])
 with ZipFile(SITE/'downloads/COMP2017-projects.zip') as z:
  check(z.testzip() is None and set(z.namelist())==set(combined),'Combined project archive membership mismatch')
  for name,data in combined.items():check(z.read(name)==data,'Combined archive source mismatch '+name)
 path=json.loads((ROOT/'content/comp2017-path.json').read_text());bilingual(path,'guided path')
 check(set(path['coaches'])==topics,'Chapter coaches must cover all 24 topics')
 check(set(t for s in path['sessions'] for t in s['topics'])==topics,'Six-pass plan must cover every course topic')
 return errors,counts
if __name__=='__main__':
 errors,counts=validate_projects()
 if errors:raise SystemExit('\n'.join(errors))
 print('PASS: bilingual engineering workshops, chapter coaching, complete source and ZIP parity. '+str(counts))
