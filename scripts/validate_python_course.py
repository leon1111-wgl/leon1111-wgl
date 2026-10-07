"""Check the imported Python handbook, its teaching files and portable ZIP."""
from pathlib import Path
from zipfile import ZipFile
import ast
import json
from build_python_course import COURSE, ROOT, course_files


def validate_python_course():
    errors = []
    manifest = json.loads((COURSE / 'tools/manifest.json').read_text())
    page = (COURSE / 'index.html').read_text()
    if page.count('<article class="chapter"') != 19:
        errors.append('Python handbook: expected 19 learning units')
    if len(manifest['examples']) != 91 or len(manifest['exercises']) != 100:
        errors.append('Python handbook: example/exercise coverage changed')
    for group in ['examples', 'exercises']:
        for entry in manifest[group]:
            paths = [entry['path']] + ([entry['solution']] if group == 'exercises' else [])
            for path in paths:
                if not (COURSE / path).is_file():
                    errors.append('Python handbook: missing teaching file ' + path)
    if len(list((COURSE / 'projects').glob('*/app.py'))) != 4:
        errors.append('Python handbook: expected four complete projects')
    for path in COURSE.rglob('*.py'):
        ast.parse(path.read_text(), filename=str(path), feature_version=(3, 10))
    for marker in ['Leon', 'class="guoliang-route"', 'Python-Zero-to-Practice.zip',
                   'id="search"', 'id="export-progress"', 'id="import-progress"']:
        if marker not in page:
            errors.append('Python handbook: missing navigation or learning control ' + marker)
    if 'python-zero-to-practice/index.html' not in (ROOT / 'README.md').read_text():
        errors.append('Python handbook: missing GitHub profile entry')
    if 'python-zero-to-practice/index.html' not in (ROOT / 'site/index.html').read_text():
        errors.append('Python handbook: missing website entry')
    files = {p.relative_to(COURSE).as_posix(): p.read_bytes() for p in course_files()}
    with ZipFile(ROOT / 'site/downloads/Python-Zero-to-Practice.zip') as archive:
        expected = {'python-zero-to-practice/' + name: data for name, data in files.items()}
        if archive.testzip() or set(archive.namelist()) != set(expected):
            errors.append('Python handbook: incomplete archive')
        for name, data in expected.items():
            if archive.read(name) != data:
                errors.append('Python handbook: archive byte mismatch ' + name)
    return errors


if __name__ == '__main__':
    errors = validate_python_course()
    if errors:
        raise SystemExit('\n'.join(errors))
    print('PASS: Python handbook coverage, source syntax, homepage entries and exact ZIP contents.')
