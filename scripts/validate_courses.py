"""Check full bilingual course parity and deep-teaching blocks."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
CODES={'INFO1113':23,'COMP2017':24,'COMP2123':26,'COMP2022':24,'COMP3308':24}

def validate_courses():
 errors=[];counts={'topics':0,'examples':0,'problems':0,'insights':0}
 def check(condition,message):
  if not condition:errors.append(message)
 for code,total in CODES.items():
  editions={}
  for lang,path in [('en',ROOT/'content'/f'{code}.json'),('zh',ROOT/'content'/'translations'/f'{code}.zh.json')]:
   if not path.exists():errors.append(f'{code}: missing {lang} edition');continue
   c=json.loads(path.read_text());editions[lang]=c
   check(len(c['topics'])==total,code+': changed topic coverage')
   check(c['code']==code,code+': incorrect course code')
   check(len(c['map'])>=3,code+': missing route stages')
   for stage in c['map']:check(bool(stage.get('purpose')),code+': stage lacks a learning purpose')
   if lang=='en':check(not re.search('[\u4e00-\u9fff]',json.dumps(c,ensure_ascii=False)),code+': English source has untranslated prose')
   if lang=='zh':check(bool(re.search('[\u4e00-\u9fff]',c['description'])),code+': Chinese description is not translated')
   for t in c['topics']:
    label=code+'/'+lang+'/'+t['id']
    for key in ('glossary','guided_questions','instructor_notes'):
     minimum=2 if key=='instructor_notes' else 3
     check(len(t.get(key,[]))>=minimum,label+': insufficient '+key)
    if lang=='zh':
     for key in ('title','story','principle','symbols','example','pitfall'):
      check(bool(re.search('[\u4e00-\u9fff]',t[key])),label+': missing Chinese '+key)
    if code in ('COMP2017','INFO1113','COMP2123'):check(len(t.get('code_examples',[]))>=2,label+': needs two runnable examples')
    if code in ('INFO1113','COMP2017'):
     check(any(len(x.get('syntax_notes',[]))>=3 for x in t.get('code_examples',[])),label+': needs a syntax guide')
    if code in ('COMP2022','COMP3308'):check(len(t.get('worked_problems',[]))>=2,label+': needs two worked problems')
    if code=='COMP2123':check(len(t.get('worked_problems',[]))>=1,label+': needs a worked algorithm problem')
    seen=set()
    for x in t.get('code_examples',[]):
     check(x['id'] not in seen,label+': duplicate code example');seen.add(x['id'])
     check(len(x.get('walkthrough',[]))>=3,label+': incomplete code walkthrough')
     check(bool(x.get('explanation')) and bool(x.get('output')),label+': code lacks explanation/output')
     if x.get('trace'):
      check(bool(x['trace']['rows']),label+': empty trace')
      for row in x['trace']['rows']:check(len(row)==len(x['trace']['columns']),label+': malformed trace row')
    for x in t.get('worked_problems',[]):
     for key in ('title','question','strategy','answer','sanity_check'):check(bool(x.get(key)),label+': problem missing '+key)
     check(len(x.get('steps',[]))>=3,label+': too few reasoning steps')
    if lang=='en':
     counts['topics']+=1;counts['examples']+=len(t.get('code_examples',[]));counts['problems']+=len(t.get('worked_problems',[]));counts['insights']+=len(t.get('instructor_notes',[]))
  if len(editions)!=2:continue
  en=editions['en'];zh=editions['zh']
  check([t['id'] for t in en['topics']]==[t['id'] for t in zh['topics']],code+': topic order differs between languages')
  check([s['topics'] for s in en['map']]==[s['topics'] for s in zh['map']],code+': route differs between languages')
  check(len(en['cheatsheet'])==len(zh['cheatsheet']),code+': reference length differs')
  for a,b in zip(en['topics'],zh['topics']):
   label=code+'/'+a['id']
   for key in ('glossary','guided_questions','instructor_notes','code_examples','worked_problems'):
    check(len(a.get(key,[]))==len(b.get(key,[])),label+': missing translated '+key)
   for x,y in zip(a.get('code_examples',[]),b.get('code_examples',[])):
    for key in ('id','code','output'):check(x[key]==y[key],label+': '+key+' differs between editions')
    check(len(x.get('walkthrough',[]))==len(y.get('walkthrough',[])),label+': walkthrough translation incomplete')
 return errors,counts

if __name__=='__main__':
 errors,counts=validate_courses()
 if errors:raise SystemExit('\n'.join(errors))
 print('PASS: full bilingual course structure and detailed teaching blocks. '+str(counts))
