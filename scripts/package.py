#!/usr/bin/env python3
"""Package only the reviewed public project, excluding local runtime artifacts."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import hashlib,json,re
ROOT=Path(__file__).resolve().parents[1]
EXCLUDED={'tmp','__pycache__','.git','.DS_Store','.venv'}
def selected():
 for p in sorted(ROOT.rglob('*')):
  if not p.is_file() or any(x in EXCLUDED for x in p.relative_to(ROOT).parts) or 'output/previews/' in p.relative_to(ROOT).as_posix() or p.suffix=='.pyc' or (p.suffix=='.log' and not ('comp2017-log-analyzer' in p.parts and p.parent.name=='fixtures')):continue
  yield p
if __name__=='__main__':
 archive=ROOT.parent/'Guoliang-GitHub-Learning-Kit.zip'
 files=list(selected())
 for p in files:
  relative=p.relative_to(ROOT)
  if re.search(r'BUSS|(?<![a-z])assignments?(?![a-z])|exam.?solution|source-review|Guoliang_Wang_CV',str(relative),re.I):raise SystemExit('Unexpected file: '+str(relative))
  if p.suffix=='.pdf' and not (p.name.endswith('-cheatsheet.pdf') or p.name=='guoliang-cheatsheet-collection.pdf'):raise SystemExit('Unexpected PDF: '+str(relative))
 with ZipFile(archive,'w',ZIP_DEFLATED,compresslevel=9) as z:
  for p in files:z.write(p,Path(ROOT.name)/p.relative_to(ROOT))
 with ZipFile(archive) as z:
  assert z.testzip() is None
 print(json.dumps({'archive':str(archive),'files':len(files),'size_mb':round(archive.stat().st_size/1e6,2),'sha256':hashlib.sha256(archive.read_bytes()).hexdigest()},indent=2))
