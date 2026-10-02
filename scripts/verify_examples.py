#!/usr/bin/env python3
"""Run every exported teaching example and compare its actual printed output."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from tempfile import TemporaryDirectory
import json,os,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'site'

def verify(entry):
 path=(SITE/entry['path']).resolve()
 if not path.is_relative_to((SITE/'examples').resolve()) or path.suffix!='.py':
  return entry['path']+': unsafe example path'
 try:
  with TemporaryDirectory(prefix='guoliang-example-') as cwd:
   result=subprocess.run([sys.executable,'-I',str(path)],cwd=cwd,capture_output=True,text=True,timeout=15,env={**os.environ,'OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','PYTHONHASHSEED':'0'})
  if result.returncode:return entry['path']+': failed\n'+result.stderr
  if result.stdout.strip()!=entry['output'].strip():
   return entry['path']+f': output mismatch\nExpected: {entry["output"]!r}\nActual: {result.stdout!r}'
 except (OSError,subprocess.TimeoutExpired) as error:return entry['path']+': '+str(error)
 return None

if __name__=='__main__':
 entries=json.loads((SITE/'examples'/'manifest.json').read_text())
 paths=[x['path'] for x in entries]
 if len(set(paths))!=len(paths):raise SystemExit('Duplicate exported example paths')
 actual={str(p.relative_to(SITE)) for p in (SITE/'examples').rglob('*.py')}
 if actual!=set(paths):raise SystemExit('Exported Python files do not match the manifest')
 with ThreadPoolExecutor(max_workers=4) as pool:errors=[r for r in pool.map(verify,entries) if r]
 if errors:raise SystemExit('\n'.join(errors))
 print(f'PASS: {len(entries)} Python examples executed in isolated temporary directories; all printed outputs matched.')
