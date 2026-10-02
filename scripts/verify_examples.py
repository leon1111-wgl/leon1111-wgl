#!/usr/bin/env python3
"""Compile/run every exported teaching program and check its real stdout."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from tempfile import TemporaryDirectory
import json,os,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];SITE=ROOT/'site'

def java_tools():
 home=os.environ.get('JAVA_HOME')
 if not home and sys.platform=='darwin':
  result=subprocess.run(['/usr/libexec/java_home','-v','1.8'],capture_output=True,text=True)
  if result.returncode==0:home=result.stdout.strip()
 if home and (Path(home)/'bin/javac').exists():return str(Path(home)/'bin/javac'),str(Path(home)/'bin/java')
 return shutil.which('javac'),shutil.which('java')

JAVA=java_tools()

def verify(entry):
 path=(SITE/entry['path']).resolve();language=entry.get('language','python')
 if language not in ('python','java','c') or not path.is_relative_to((SITE/'examples').resolve()) or path.suffix!={'python':'.py','java':'.java','c':'.c'}[language]:
  return entry['path']+': unsafe example path or language'
 try:
  with TemporaryDirectory(prefix='guoliang-example-') as cwd:
   env={**os.environ,'OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','PYTHONHASHSEED':'0'}
   if language=='python':command=[sys.executable,'-I',str(path)]
   else:
    source=Path(cwd)/path.name;shutil.copy2(path,source)
    if language=='java':
     if not all(JAVA):return 'Java JDK unavailable: install a JDK and set JAVA_HOME'
     compile_command=[JAVA[0],'-encoding','UTF-8','-Xlint:all',str(source)]
     command=[JAVA[1],'-ea','-cp',cwd,'Main']
    else:
     compiler=shutil.which('clang') or shutil.which('cc')
     if not compiler:return 'C compiler unavailable'
     executable=Path(cwd)/'demo'
     compile_command=[compiler,'-std=c11','-Wall','-Wextra','-Werror','-pedantic','-pthread',str(source),'-lm','-o',str(executable)]
     command=[str(executable)]
    compiled=subprocess.run(compile_command,cwd=cwd,capture_output=True,text=True,timeout=30,env=env)
    if compiled.returncode:return entry['path']+': compilation failed\n'+compiled.stderr
   result=subprocess.run(command,cwd=cwd,capture_output=True,text=True,timeout=15,env=env)
  if result.returncode:return entry['path']+': execution failed\n'+result.stderr
  # A text block may omit its one final newline. Preserve all other whitespace.
  if result.stdout.removesuffix('\n')!=entry['output'].removesuffix('\n'):return entry['path']+f': output mismatch\nExpected: {entry["output"]!r}\nActual: {result.stdout!r}'
 except (OSError,subprocess.TimeoutExpired) as error:return entry['path']+': '+str(error)
 return None

if __name__=='__main__':
 entries=json.loads((SITE/'examples'/'manifest.json').read_text());paths=[x['path'] for x in entries]
 if len(set(paths))!=len(paths):raise SystemExit('Duplicate exported example paths')
 actual={str(p.relative_to(SITE)) for p in (SITE/'examples').rglob('*') if p.suffix in ('.py','.c','.java')}
 if actual!=set(paths):raise SystemExit('Exported source files do not match manifest: '+repr(actual.symmetric_difference(set(paths))))
 with ThreadPoolExecutor(max_workers=4) as pool:errors=[r for r in pool.map(verify,entries) if r]
 if errors:raise SystemExit('\n'.join(errors))
 counts={language:sum(x.get('language','python')==language for x in entries) for language in ('python','java','c')}
 print(f'PASS: {len(entries)} examples compiled/executed in isolated temporary directories; all printed outputs matched. {counts}')
