#!/usr/bin/env python3
"""Verify that copied HTML code and both downloadable archives match their sources."""
from pathlib import Path
from html.parser import HTMLParser
from zipfile import ZipFile
import json
ROOT=Path(__file__).resolve().parents[1];SITE=ROOT/'site'

class CodeBlocks(HTMLParser):
 def __init__(self):super().__init__();self.code={};self.active=None
 def handle_starttag(self,tag,attrs):
  attr=dict(attrs)
  if tag=='code' and attr.get('id','').startswith('code-'):
   self.active=attr['id'];self.code[self.active]=''
 def handle_endtag(self,tag):
  if tag=='code':self.active=None
 def handle_data(self,data):
  if self.active:self.code[self.active]+=data

errors=[];blocks=0
for source in sorted((ROOT/'content').glob('COMP*.json'))+[ROOT/'content/INFO1113.json']+sorted((ROOT/'content/paths').glob('*.json'))+[ROOT/'content/primer.json']:
 c=json.loads(source.read_text());ai=isinstance(c.get('title'),dict)
 for lang in ('en','zh'):
  page=SITE/'ai'/f'{c["id"]}.{lang}.html' if ai else SITE/'courses'/(c['code'].lower()+('.zh' if lang=='zh' else '')+'.html')
  parser=CodeBlocks();parser.feed(page.read_text());expected={}
  for t in c['topics']:
   for x in t.get('code_examples',[]):expected['code-'+t['id']+'-'+x['id']]=x['code'].removesuffix('\n')
  actual={k:v.removesuffix('\n') for k,v in parser.code.items()}
  if actual!=expected:errors.append(str(page.relative_to(SITE))+': copied code differs from source')
  blocks+=len(actual)
manifest=json.loads((SITE/'examples/manifest.json').read_text())
for name,entries in [('guoliang-code-examples.zip',manifest),('guoliang-python-examples.zip',[x for x in manifest if x['language']=='python'])]:
 with ZipFile(SITE/'downloads'/name) as z:
  if z.testzip() is not None:errors.append(name+': corrupt archive')
  if json.loads(z.read('examples/manifest.json'))!=entries:errors.append(name+': manifest mismatch')
  expected={'examples/README.md','examples/manifest.json'}|{x['path'] for x in entries}
  if set(z.namelist())!=expected:errors.append(name+': missing or extra archive files')
  for x in entries:
   if z.read(x['path'])!=(SITE/x['path']).read_bytes():errors.append(name+': source mismatch '+x['path'])
if errors:raise SystemExit('\n'.join(errors))
print(f'PASS: {blocks} rendered code blocks preserve the original source; both ZIP archives match their manifests and source files.')
