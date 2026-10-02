#!/usr/bin/env python3
"""Validate deliverable scope, navigation and one-page PDF structure."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote,urlparse
import json,re,sys
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1];SITE=ROOT/'site'
CODES=['INFO1113','COMP2017','COMP2123','COMP2022','COMP3308'];errors=[]
class Page(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.links=[];self.language=None
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='html':self.language=a.get('lang')
  if 'id' in a:self.ids.append(a['id'])
  if tag in ['a','link'] and a.get('href'):self.links.append(a['href'])
  if tag in ['img','script'] and a.get('src'):self.links.append(a['src'])
def check(condition,message):
 if not condition:errors.append(message)
parsers={}
for f in SITE.rglob('*.html'):
 p=Page();p.feed(f.read_text());parsers[f.resolve()]=p
 check(p.language==('zh-Hans' if f.name.endswith('.zh.html') else 'en'),f'{f.name}: incorrect page language')
 check(len(p.ids)==len(set(p.ids)),f'{f.name}: duplicate IDs')
for f,p in parsers.items():
 for link in p.links:
  parsed=urlparse(link)
  if parsed.scheme or link.startswith('//'):continue
  dest=(f.parent/unquote(parsed.path)).resolve() if parsed.path else f
  check(dest.exists(),f'{f.relative_to(ROOT)} broken link {link}')
  if parsed.fragment and dest.suffix=='.html':
   check(dest in parsers and unquote(parsed.fragment) in parsers[dest].ids,f'{f.name} missing anchor {link}')
for code in CODES:
 c=json.loads((ROOT/'content'/f'{code}.json').read_text())
 topics=c['topics'];ids=[t['id'] for t in topics]
 check(len(ids)==len(set(ids)),code+' duplicate topic ids')
 mapped=[k for s in c['map'] for k in s['topics']]
 check(set(ids)==set(mapped),code+' missing or extra knowledge map entries')
 for t in topics:
  for key in ['title','story','principle','formula','symbols','example','pitfall','check']:
   check(bool(t.get(key)),code+' '+t['id']+' missing '+key)
  check(all(t['check'].get(k) for k in ['question','answer']),code+' check malformed')
 if code=='COMP2123':
  check(len(topics)==26,code+' topic coverage changed')
  for t in topics:
   for key,minimum in [('code_examples',1),('glossary',3),('guided_questions',3)]:
    check(len(t.get(key,[]))>=minimum,code+' '+t['id']+' insufficient '+key)
 text=json.dumps(c,ensure_ascii=False)
 check(not re.search('[\u4e00-\u9fff]',text),code+' non-English content')
 check(not re.search(r'BUSS[0-9]{4}',text,re.I),code+' excluded course in JSON')
 pdf=SITE/'downloads'/f'{code}-cheatsheet.pdf';r=PdfReader(pdf)
 check(len(r.pages)==1,code+' PDF not one page')
 check('Guoliang' in r.pages[0].extract_text(),code+' missing watermark')
 check(pdf.stat().st_size>10000,code+' empty-looking PDF')
for f in list(SITE.rglob('*'))+list((ROOT/'notes').rglob('*.md'))+[ROOT/'README.md']:
 if not f.is_file():continue
 check(not re.search(r'BUSS|assignment|exam.?solutions',f.name,re.I),'Excluded filename '+str(f))
 if f.suffix in ['.html','.md','.css','.js','.svg']:
  s=f.read_text();check(not re.search(r'BUSS[0-9]{4}',s,re.I),'Excluded course content '+str(f))
  bilingual=(any(part in ('ai','courses','cheatsheets','notes','maps','projects','project-code') for part in f.relative_to(ROOT).parts) or f.name=='app.js')
  if not bilingual:check(not re.search('[\u4e00-\u9fff]',s),'Non-English original course text '+str(f))
  check('TODO' not in s and 'Lorem ipsum' not in s,'Placeholder '+str(f))
for f in [ROOT/'README.md']+list((ROOT/'notes').glob('*.md')):
 # Generated notes use triple-backtick blocks and single-backtick code spans.
 # C calls such as operations[index](17, 6) inside code are not links.
 prose=re.sub(r'^```[^\n]*\n.*?^```[^\n]*(?:\n|$)','',f.read_text(),flags=re.M|re.S)
 prose=re.sub(r'`[^`\n]*`','',prose)
 for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',prose):
  parsed=urlparse(target)
  if parsed.scheme or target.startswith('#'):continue
  check((f.parent/unquote(parsed.path)).exists(),f'{f.name} broken Markdown target {target}')
collection=PdfReader(SITE/'downloads'/'guoliang-cheatsheet-collection.pdf')
check(len(collection.pages)==5,'Collection must contain five single-page references')
from validate_paths import validate_paths
path_errors,guides=validate_paths()
errors.extend(path_errors)
from validate_courses import validate_courses
course_errors,counts=validate_courses()
errors.extend(course_errors)
from validate_projects import validate_projects
project_errors,project_counts=validate_projects()
errors.extend(project_errors)
for folder in ('courses','ai','projects'):
 for f in (SITE/folder).glob('*.html'):
  page=f.read_text()
  check('class="learning-route"' in page,f.name+' missing opening roadmap')
  check(page.index('class="learning-route"')<page.index('class="course-layout"'),f.name+' roadmap is too late')
for f in (SITE/'notes').glob('*.md'):
 check('assets/maps/' in f.read_text()[:1200],f.name+' missing opening roadmap in downloaded notes')
if errors:
 print('\n'.join(errors));sys.exit(1)
print(f'PASS: {len(parsers)} HTML pages, local links and anchors, opening roadmaps, five full bilingual courses and bilingual AI guides, excluded source content, five single-page PDFs and collection; course detail: {counts}; project detail: {project_counts}.')
