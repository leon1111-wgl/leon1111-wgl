"""Build the supplied Python handbook and a complete portable learning ZIP."""
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED
import os
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / 'site/python-zero-to-practice'


def course_files():
    return sorted(p for p in COURSE.rglob('*') if p.is_file()
                  and '__pycache__' not in p.parts and p.suffix != '.pyc')


def build():
    subprocess.run([sys.executable, str(COURSE / 'source/build.py')],
                   check=True, env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
    target = ROOT / 'site/downloads/Python-Zero-to-Practice.zip'
    with ZipFile(target, 'w', ZIP_DEFLATED, compresslevel=9) as archive:
        for path in course_files():
            name = 'python-zero-to-practice/' + path.relative_to(COURSE).as_posix()
            info = ZipInfo(name, (2026, 10, 7, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, path.read_bytes())
    print(f'Built Python handbook and portable ZIP ({len(course_files())} files).')


if __name__ == '__main__':
    build()
