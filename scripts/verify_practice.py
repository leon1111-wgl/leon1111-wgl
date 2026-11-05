#!/usr/bin/env python3
"""Run everything checkable in content/practice/*.json: model answers against their tests, tests against wrong answers,
trace tables against instrumented programs, numeric answers against their calculation.

    python3 scripts/verify_practice.py [course ...]
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PACKS = ROOT / 'content' / 'practice'
CC = shutil.which('clang') or shutil.which('cc')
HEADERS = {'stdio.h', 'stdlib.h', 'string.h', 'stdint.h', 'stdbool.h', 'ctype.h', 'limits.h', 'assert.h', 'math.h', 'stddef.h'}
JAVA_FORBIDDEN = ('String.format', 'printf(', 'Scanner', '.stream()')


def run_program(language, code, tests=None, java_tests_name='Tests'):
    """Return (ok, stdout, stderr). ok is False on a compile failure, a crash or a non-zero exit."""
    with TemporaryDirectory(prefix='leon-practice-') as tmp:
        tmp = Path(tmp)
        try:
            if language == 'c':
                (tmp / 'main.c').write_text(code + ('\n' + tests if tests else ''))
                done = subprocess.run([CC, '-std=c11', '-Wall', '-Wextra', '-Werror', '-pedantic', 'main.c', '-lm', '-o', 'demo'], cwd=tmp, capture_output=True, text=True, timeout=30)
                if done.returncode:
                    return False, '', 'compile: ' + done.stderr
                done = subprocess.run(['./demo'], cwd=tmp, capture_output=True, text=True, timeout=10)
            elif language == 'java':
                (tmp / 'Main.java').write_text(code)
                files = ['Main.java']
                if tests:
                    (tmp / f'{java_tests_name}.java').write_text(tests)
                    files.append(f'{java_tests_name}.java')
                done = subprocess.run(['javac', '-encoding', 'UTF-8', *files], cwd=tmp, capture_output=True, text=True, timeout=60)
                if done.returncode:
                    return False, '', 'compile: ' + done.stderr
                done = subprocess.run(['java', '-ea', '-cp', '.', java_tests_name if tests else 'Main'], cwd=tmp, capture_output=True, text=True, timeout=15)
            else:
                (tmp / 'main.py').write_text(code + ('\n' + tests if tests else ''))
                done = subprocess.run([sys.executable, '-I', 'main.py'], cwd=tmp, capture_output=True, text=True, timeout=15)
        except subprocess.TimeoutExpired:
            return False, '', 'timeout'
        return done.returncode == 0, done.stdout, done.stderr


def same(a, b):
    return a.rstrip('\n') == b.rstrip('\n')


def check_question(q):
    errors = []
    where = q['id']
    kind = q['kind']
    language = q.get('language', 'python')
    if kind in ('write', 'bug'):
        model = q['model_code'] if kind == 'write' else q['fixed_code']
        wrong = q['wrong_code'] if kind == 'write' else q['code']
        ok, out, err = run_program(language, model, q['tests'])
        if not ok:
            errors.append(f'{where}: model answer failed: {err[:400]}')
        elif not same(out, q['expected']):
            errors.append(f'{where}: output {out[:200]!r} != expected {q["expected"][:200]!r}')
        ok, out, err = run_program(language, wrong, q['tests'])
        if ok and same(out, q['expected']):
            errors.append(f'{where}: the tests also pass on the wrong answer, so they prove nothing')
        if language == 'c':
            import re
            for h in re.findall(r'#include\s*<([^>]+)>', model + q['tests']):
                if h not in HEADERS:
                    errors.append(f'{where}: <{h}> is not available to the browser runner')
        if language == 'java':
            for word in JAVA_FORBIDDEN:
                if word in model or word in q['tests']:
                    errors.append(f'{where}: avoid {word} (browser Java)')
    if kind == 'predict':
        ok, out, err = run_program(language, q['code'])
        if not ok or not same(out, q['output']):
            errors.append(f'{where}: output {out[:200]!r} != {q["output"][:200]!r} {err[:200]}')
    if kind == 'trace':
        ok, out, err = run_program(q.get('verify_language', 'python'), q['verify_code'])
        if not ok:
            errors.append(f'{where}: verify_code failed: {err[:300]}')
        else:
            got = [line.split('\t') for line in out.rstrip('\n').split('\n')]
            if got != q['rows']:
                errors.append(f'{where}: trace rows differ\n  table: {q["rows"]}\n  ran:   {got}')
    if kind == 'numeric':
        ok, out, err = run_program('python', q['verify_code'])
        if not ok:
            errors.append(f'{where}: verify_code failed: {err[:300]}')
        else:
            try:
                value = float(out.strip().split()[-1])
                if abs(value - q['answer']) > (q.get('tolerance') or 0) + 1e-9:
                    errors.append(f'{where}: computed {value}, question says {q["answer"]} (tolerance {q.get("tolerance", 0)})')
            except ValueError:
                errors.append(f'{where}: verify_code must print a number, got {out[:80]!r}')
    if q.get('verify_output') is not None and kind not in ('trace', 'numeric'):
        ok, out, err = run_program(q.get('verify_language', 'python'), q['verify_code'])
        if not ok or not same(out, q['verify_output']):
            errors.append(f'{where}: verify_code output {out[:200]!r} != {q["verify_output"][:200]!r} {err[:200]}')
    return errors


def main():
    names = sys.argv[1:] or sorted(p.stem for p in PACKS.glob('*.json'))
    total = 0
    problems = []
    for name in names:
        path = PACKS / f'{name}.json'
        if not path.exists():
            problems.append(f'{name}: no pack')
            continue
        pack = json.loads(path.read_text())
        with ThreadPoolExecutor(max_workers=4) as pool:
            for errs in pool.map(check_question, pack['questions']):
                problems.extend(f'{name}/{e}' for e in errs)
        total += len(pack['questions'])
    if problems:
        print('\n'.join(problems))
        raise SystemExit(1)
    print(f'PASS: {total} practice questions checked by running them')


if __name__ == '__main__':
    main()
