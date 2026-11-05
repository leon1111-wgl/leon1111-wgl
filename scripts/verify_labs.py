#!/usr/bin/env python3
"""Run every engineering lab with its real tools and check what it claims.

    python3 scripts/verify_labs.py [lab ...]            check each step's exit code and expected text
    python3 scripts/verify_labs.py --write [lab ...]    also save the output to captured.json, which the page shows
"""
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import os
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
LABS = ROOT / 'content' / 'labs'


def normalise(text, tmp):
    text = text.replace(str(tmp), '.').replace(os.path.realpath(tmp), '.')
    text = re.sub(r'0x[0-9a-fA-F]{6,}', '0xADDR', text)
    text = re.sub(r'==\d+==', '==PID==', text)
    return text.rstrip() + '\n'


def run_lab(folder, write):
    lab = json.loads((folder / 'lab.json').read_text())
    errors, captured = [], {}
    with TemporaryDirectory(prefix='leon-lab-') as tmp:
        tmp = Path(tmp)
        if (folder / 'files').exists():
            shutil.copytree(folder / 'files', tmp, dirs_exist_ok=True)
        for i, step in enumerate(lab['steps']):
            patch = step.get('patch')
            if patch:
                target = tmp / patch['file']
                text = target.read_text()
                if patch['from'] not in text:
                    errors.append(f'{lab["id"]} step {i}: patch text not found in {patch["file"]}')
                    continue
                target.write_text(text.replace(patch['from'], patch['to'], 1))
            if not step.get('command'):
                continue
            env = {**os.environ, 'ASAN_OPTIONS': 'color=never', 'TSAN_OPTIONS': 'color=never', 'PYTHONHASHSEED': '0', 'NO_COLOR': '1', 'PYTHONDONTWRITEBYTECODE': '1'}
            done = subprocess.run(['bash', '-c', step['command']], cwd=tmp, env=env, capture_output=True, text=True, timeout=180)
            out = normalise(done.stdout + (('\n' if done.stdout and done.stderr else '') + done.stderr), tmp)
            want = step.get('exit', 0)
            if done.returncode != want:
                errors.append(f'{lab["id"]} step {i}: exit {done.returncode}, expected {want}\n{out[-900:]}')
            for text in step.get('contains', []):
                if text not in out:
                    errors.append(f'{lab["id"]} step {i}: missing {text!r}\n{out[-900:]}')
            captured[str(i)] = out
    if write and not errors:
        (folder / 'captured.json').write_text(json.dumps(captured, ensure_ascii=False, indent=1))
    return errors


def main():
    args = sys.argv[1:]
    write = '--write' in args
    names = [a for a in args if not a.startswith('--')]
    folders = [LABS / n for n in names] if names else sorted(p for p in LABS.iterdir() if (p / 'lab.json').exists())
    errors = []
    for folder in folders:
        problems = run_lab(folder, write)
        errors.extend(problems)
        print(('FAIL ' if problems else 'ok   ') + folder.name)
    if errors:
        print('\n'.join(errors))
        raise SystemExit(1)
    print(f'PASS: {len(folders)} labs ran with their real tools')


if __name__ == '__main__':
    main()
