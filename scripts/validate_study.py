#!/usr/bin/env python3
"""Check site/learn/data against the lessons: every reference resolves, marks add up, both languages present, no answer leaks."""
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'site' / 'learn' / 'data'
sys.path.insert(0, str(ROOT / 'scripts'))
from build_learn import catalogue

KINDS = {'predict', 'worked', 'mcq', 'numeric', 'trace', 'write', 'memory', 'short', 'bug', 'proof', 'design'}
SELF_MARKED = {'write', 'memory', 'short', 'bug', 'proof', 'design'}
BANNED = re.compile(r'past[- ]paper|往年|真题|will (?:be|appear) (?:in|on) the exam|一定会考|必考|考试会考', re.I)


def two(value, where, errors, optional=False):
    if value is None and optional:
        return
    if not (isinstance(value, dict) and value.get('en') and value.get('zh')):
        errors.append(f'{where}: needs both en and zh')


def validate_study():
    errors = []
    courses = {c['id']: c for c in catalogue()['courses']}
    manifest = {e['path'] for e in json.loads((ROOT / 'site' / 'examples' / 'manifest.json').read_text())}
    totals = {'cards': 0, 'questions': 0, 'papers': 0, 'labs': 0}
    for f in sorted(DATA.glob('*.json')):
        if f.name in ('keywords.json', 'summary.json') or f.name.startswith('terms-'):
            continue
        d = json.loads(f.read_text())
        cid = d['course']
        if cid not in courses:
            errors.append(f'{f.name}: unknown course')
            continue
        chapters = {c['id'] for c in courses[cid]['chapters']}
        ids = [q['id'] for q in d['questions']]
        if len(ids) != len(set(ids)):
            errors.append(f'{cid}: duplicate question id')
        card_ids = [c['id'] for c in d['cards']]
        if len(card_ids) != len(set(card_ids)):
            errors.append(f'{cid}: duplicate card id')
        for c in d['cards']:
            if c['topic'] not in chapters:
                errors.append(f'{cid}/{c["id"]}: unknown chapter')
            two(c['q'], f'{cid}/{c["id"]} q', errors)
            two(c['a'], f'{cid}/{c["id"]} a', errors)
        by_id = {}
        for q in d['questions']:
            where = f'{cid}/{q["id"]}'
            by_id[q['id']] = q
            if q['kind'] not in KINDS:
                errors.append(f'{where}: unknown kind {q["kind"]}')
            if q['topic'] not in chapters:
                errors.append(f'{where}: unknown chapter {q["topic"]}')
            two(q['title'], f'{where} title', errors)
            if not isinstance(q.get('marks'), int) or q['marks'] < 1:
                errors.append(f'{where}: marks must be a positive integer')
            kind = q['kind']
            if kind == 'mcq':
                correct = [o for o in q['options'] if o.get('correct')]
                if len(correct) != 1:
                    errors.append(f'{where}: needs exactly one correct option')
                for o in q['options']:
                    two(o['text'], f'{where} option', errors)
                    two(o.get('why'), f'{where} option why', errors, optional=True)
            if kind == 'numeric' and not isinstance(q.get('answer'), (int, float)):
                errors.append(f'{where}: numeric answer must be a number')
            if kind == 'trace':
                columns = q['columns']
                two(columns, f'{where} columns', errors)
                width = len(columns['en'])
                if len(columns['zh']) != width or any(len(r) != width for r in q['rows']):
                    errors.append(f'{where}: trace rows and columns disagree')
            if kind in SELF_MARKED:
                if not q.get('rubric'):
                    errors.append(f'{where}: needs a rubric')
                else:
                    if sum(r['marks'] for r in q['rubric']) != q['marks']:
                        errors.append(f'{where}: rubric marks do not add up to {q["marks"]}')
                    for r in q['rubric']:
                        two(r['text'], f'{where} rubric', errors)
                if not (q.get('model_code') or q.get('solution') or q.get('memory')):
                    errors.append(f'{where}: needs a model answer')
                for m in q.get('mistakes', []):
                    two(m, f'{where} mistake', errors)
            if kind == 'write' and not q.get('language'):
                errors.append(f'{where}: needs a language')
            for field in ('prompt', 'question', 'solution'):
                if field in q:
                    two(q[field], f'{where} {field}', errors)
            if BANNED.search(json.dumps(q, ensure_ascii=False)):
                errors.append(f'{where}: must not claim knowledge of a real exam or refer to past papers')
        for p in d['papers']:
            where = f'{cid}/paper {p["id"]}'
            if BANNED.search(json.dumps(p, ensure_ascii=False)):
                errors.append(f'{where}: must not claim knowledge of a real exam or refer to past papers')
            two(p['title'], where, errors)
            if not p.get('minutes') or not p.get('questions'):
                errors.append(f'{where}: needs minutes and questions')
            missing = [x for x in p['questions'] if x not in by_id]
            if missing:
                errors.append(f'{where}: unknown questions {missing}')
            if len(p['questions']) != len(set(p['questions'])):
                errors.append(f'{where}: repeats a question')
        for lab in d['labs']:
            two(lab['title'], f'{cid}/lab {lab["id"]}', errors)
            two(lab['scenario'], f'{cid}/lab {lab["id"]} scenario', errors)
        totals['cards'] += len(d['cards'])
        totals['questions'] += len(d['questions'])
        totals['papers'] += len(d['papers'])
        totals['labs'] += len(d['labs'])
    runnable = json.loads((ROOT / 'content' / 'browser-runnable.json').read_text())
    errors.extend(f'browser-runnable.json lists an unknown example: {p}' for p in runnable if p not in manifest)
    return errors, totals


if __name__ == '__main__':
    problems, counts = validate_study()
    if problems:
        print('\n'.join(problems[:60]))
        raise SystemExit(1)
    print('PASS: study data', counts)
