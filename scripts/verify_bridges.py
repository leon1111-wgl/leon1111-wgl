#!/usr/bin/env python3
"""Compile and run every example in the first-steps guides, and check both languages are complete."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_practice import run_program, same

SOURCE = Path(__file__).resolve().parents[1] / 'content' / 'bridges'


def two(value, where, errors):
    if not (isinstance(value, dict) and value.get('en') and value.get('zh')):
        errors.append(f'{where}: needs en and zh')


def check_example(item):
    where, e = item
    ok, out, err = run_program(e['language'], e['code'])
    if not ok:
        return f'{where}: failed: {err[:300]}'
    if not same(out, e['output']):
        return f'{where}: printed {out[:200]!r}, page says {e["output"][:200]!r}'
    return None


def main():
    names = sys.argv[1:]
    paths = [SOURCE / f'{n}.json' for n in names] if names else sorted(SOURCE.glob('*.json'))
    errors, examples = [], []
    for path in paths:
        g = json.loads(path.read_text())
        name = g['id']
        two(g['title'], f'{name} title', errors)
        two(g['summary'], f'{name} summary', errors)
        if g['kind'] not in ('first-steps', 'by-hand'):
            errors.append(f'{name}: unknown kind')
        ids = [x['id'] for x in g['lessons']]
        if len(ids) != len(set(ids)):
            errors.append(f'{name}: duplicate lesson id')
        for lesson in g['lessons']:
            where = f'{name}/{lesson["id"]}'
            for field in ('title', 'goal', 'plain'):
                two(lesson.get(field), f'{where} {field}', errors)
            if len(lesson.get('mistakes', [])) < 2:
                errors.append(f'{where}: needs at least two mistakes')
            if len(lesson.get('check', [])) < 2:
                errors.append(f'{where}: needs at least two checks')
            if g['kind'] == 'first-steps' and not lesson.get('example'):
                errors.append(f'{where}: first-steps lessons need an example')
            for c in lesson.get('check', []):
                two(c['q'], f'{where} check q', errors)
                two(c['a'], f'{where} check a', errors)
            for m in lesson.get('mistakes', []):
                two(m['why'], f'{where} mistake', errors)
            if lesson.get('example'):
                examples.append((where, lesson['example']))
                walk = lesson['example'].get('walk', {})
                if len(walk.get('en', [])) != len(walk.get('zh', [])):
                    errors.append(f'{where}: walkthrough lengths differ')
    with ThreadPoolExecutor(max_workers=4) as pool:
        errors.extend(e for e in pool.map(check_example, examples) if e)
    if errors:
        print('\n'.join(errors))
        raise SystemExit(1)
    print(f'PASS: {len(paths)} guides, {len(examples)} examples compiled, run and matched')


if __name__ == '__main__':
    main()
