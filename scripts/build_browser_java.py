#!/usr/bin/env python3
"""Write site/assets/runner/java/ from a teavm-javac build, adding the few classes its library lacks.

    python3 scripts/build_browser_java.py <folder with the build's compiler.wasm, compiler.wasm-runtime.js and two .bin archives>

Upstream's class library has no Scanner, StringJoiner or InputMismatchException. scripts/java_shims holds small original
versions: javac sees them under their real names in the compile archive, and TeaVM finds them under its T-prefixed names in the
runtime archive. An archive is gzip around records of: 2-byte name length, name, 4-byte size, bytes. Needs a local JDK.
"""
from pathlib import Path
import gzip
import re
import shutil
import struct
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SHIMS = ROOT / 'scripts' / 'java_shims'
OUT = ROOT / 'site' / 'assets' / 'runner' / 'java'
NAMES = ('Scanner', 'StringJoiner', 'InputMismatchException')


def javac(sources, out):
    subprocess.run(['javac', '-nowarn', '-source', '8', '-target', '8', '-d', str(out), *map(str, sources)], check=True, capture_output=True)


def add_classes(source, target, classes):
    data = gzip.decompress(source.read_bytes())
    extra = bytearray()
    for f in sorted(classes.rglob('*.class')):
        name = f.relative_to(classes).as_posix().encode()
        body = f.read_bytes()
        extra += struct.pack('>H', len(name)) + name + struct.pack('>I', len(body)) + body
    target.write_bytes(gzip.compress(data + bytes(extra), 9, mtime=0))


def main():
    build = Path(sys.argv[1])
    OUT.mkdir(parents=True, exist_ok=True)
    shutil.copy(build / 'compiler.wasm', OUT / 'compiler.wasm')
    shutil.copy(build / 'compiler.wasm-runtime.js', OUT / 'compiler.wasm-runtime.js')
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        plain = tmp / 'plain'; plain.mkdir()
        javac(sorted((SHIMS / 'java' / 'util').glob('*.java')), plain)
        add_classes(build / 'compile-classlib-teavm.bin', OUT / 'compile-classlib.bin', plain)
        src = tmp / 'renamed' / 'org' / 'teavm' / 'classlib' / 'java' / 'util'
        src.mkdir(parents=True)
        renamed = tmp / 'renamed-classes'; renamed.mkdir()
        for name in NAMES:
            text = (SHIMS / 'java' / 'util' / f'{name}.java').read_text()
            text = text.replace('package java.util;', 'package org.teavm.classlib.java.util;\nimport java.util.*;')
            for other in NAMES:
                text = re.sub(rf'\b{other}\b', f'T{other}', text)
            (src / f'T{name}.java').write_text(text)
        javac(sorted(src.glob('*.java')), renamed)
        add_classes(build / 'runtime-classlib-teavm.bin', OUT / 'runtime-classlib.bin', renamed)
    print('browser Java:', sorted(p.name for p in OUT.iterdir()))


if __name__ == '__main__':
    main()
