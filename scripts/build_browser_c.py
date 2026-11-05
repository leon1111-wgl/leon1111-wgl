#!/usr/bin/env python3
"""Write site/assets/runner/c/ from a build of xcc's wcc (public/wccfiles.zip and LICENSE).

    python3 scripts/build_browser_c.py <build folder>

The browser loads cc.wasm, two small libraries and the headers as one JSON file. wcc's stdio has no ferror or clearerr; here
streams are in memory and cannot fail that way, so stdio.h gains two macros. .github/workflows/build-runtimes.yml makes the build.
"""
from pathlib import Path
import json
import shutil
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'site' / 'assets' / 'runner' / 'c'
EXTRA_STDIO = '''
// added for the browser: in-memory streams here cannot report a device error
#define ferror(stream) ((void)(stream), 0)
#define clearerr(stream) ((void)(stream))
'''


def main():
    build = Path(sys.argv[1])
    OUT.mkdir(parents=True, exist_ok=True)
    headers = {}
    with zipfile.ZipFile(build / 'public' / 'wccfiles.zip') as z:
        for name in z.namelist():
            if name.startswith('usr/include/') and not name.endswith('/'):
                headers[name[len('usr/include/'):]] = z.read(name).decode()
            elif name == 'usr/bin/cc':
                (OUT / 'cc.wasm').write_bytes(z.read(name))
            elif name.startswith('usr/lib/') and name.endswith('.a'):
                (OUT / Path(name).name).write_bytes(z.read(name))
    headers['stdio.h'] += EXTRA_STDIO
    (OUT / 'include.json').write_text(json.dumps(headers, separators=(',', ':')))
    shutil.copy(build / 'LICENSE', OUT / 'LICENSE.xcc.txt')
    print('browser C:', sorted(p.name for p in OUT.iterdir()))


if __name__ == '__main__':
    main()
