"""Build projects in isolation; execute behavioral tests and documented runs."""
from pathlib import Path
from tempfile import TemporaryDirectory
from concurrent.futures import ThreadPoolExecutor
import json,os,shutil,subprocess
from build_projects import projects
ROOT=Path(__file__).resolve().parents[1]
def verify(p):
 with TemporaryDirectory(prefix='guoliang-project-') as tmp:
  folder=Path(tmp)/p['id'];shutil.copytree(ROOT/'projects'/p['id'],folder)
  env={**os.environ,'LC_ALL':'C','PYTHONHASHSEED':'0'}
  build=subprocess.run(['make','CC=clang','CFLAGS=-std=c11 -Wall -Wextra -Werror -pedantic -O1 -g -pthread'],cwd=folder,env=env,capture_output=True,text=True,timeout=45)
  if build.returncode:raise RuntimeError(p['id']+' build:\n'+build.stdout+build.stderr)
  tests=subprocess.run(['make','test'],cwd=folder,env=env,capture_output=True,text=True,timeout=90)
  if tests.returncode:raise RuntimeError(p['id']+' tests:\n'+tests.stdout+tests.stderr)
  for i,run in enumerate(p['runs'],1):
   result=subprocess.run(['/bin/sh','-c',run['command']],input=run.get('stdin'),cwd=folder,env=env,capture_output=True,text=True,timeout=15)
   if result.returncode!=run['expected_exit'] or result.stdout.removesuffix('\n')!=run['stdout'].removesuffix('\n'):
    raise RuntimeError(f'{p["id"]} documented run {i}: expected exit {run["expected_exit"]}, got {result.returncode}; expected stdout {run["stdout"]!r}, got {result.stdout!r}; stderr {result.stderr!r}')
  return p['id']+': strict build, behavior tests and '+str(len(p['runs']))+' documented runs PASS\n'+tests.stdout+tests.stderr
if __name__=='__main__':
 with ThreadPoolExecutor(max_workers=3) as pool:
  for result in pool.map(verify,projects()):print(result)
