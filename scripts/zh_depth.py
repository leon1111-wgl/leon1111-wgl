"""Chinese depth of the course chapters: measure it, show a chapter for translation, apply a translated chapter.

    python3 scripts/zh_depth.py report [CODE ...]          zh/en length per chapter
    python3 scripts/zh_depth.py check                      fail if any course has a thin chapter
    python3 scripts/zh_depth.py show CODE TOPIC            English chapter, current Chinese, and its programs
    python3 scripts/zh_depth.py apply CODE TOPIC FILE      replace the Chinese chapter's prose with FILE

The measure is Chinese characters divided by English characters over reader prose only: code, output,
ids, formulas and trace cells are left out. Chapters written in full Chinese measure 0.40 to 0.45; the
compressed older chapters measured about 0.25 to 0.30.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEEPENED = ('COMP2022', 'COMP2123', 'COMP3308', 'COMP2017', 'INFO1113')
# full translations measure 0.375 to 0.46; the compressed chapters they replaced measured 0.23 to 0.38 (a mean of 0.28 to 0.35 per course). The floor
# leaves room for a shorter standard term (德摩根律 for De Morgan 律) without letting a compressed chapter through.
FLOOR = 0.37
SKIP = {'code', 'output', 'id', 'language', 'formula', 'rows'}
HAN = re.compile('[一-鿿]')


def prose_len(x):
    if isinstance(x, str):
        return len(x)
    if isinstance(x, list):
        return sum(prose_len(i) for i in x)
    if isinstance(x, dict):
        return sum(prose_len(v) for k, v in x.items() if k not in SKIP)
    return 0


def editions(code):
    en = json.loads((ROOT / 'content' / f'{code}.json').read_text())
    zh_path = ROOT / 'content' / 'translations' / f'{code}.zh.json'
    return en, json.loads(zh_path.read_text()), zh_path


def ratios(code):
    en, zh, _ = editions(code)
    zt = {t['id']: t for t in zh['topics']}
    return [(t['id'], prose_len(zt[t['id']]) / max(1, prose_len(t))) for t in en['topics']]


def english_left(topic):
    """Runs of six or more English words in Chinese prose, outside `code` spans: untranslated sentences."""
    found = []

    def walk(x, path):
        if isinstance(x, str):
            # code spans and quoted literals (a compiler message, a Javadoc line) stay in English on purpose
            text = re.sub(r'`[^`]*`|“[^”]*”|"[^"]*"', ' ', x)
            # words of two letters or more: lists of vertex or state names such as "B, A, D, C" are not prose
            for m in re.finditer(r"(?:[A-Za-z][A-Za-z'’-]+[,;:]?\s+){5,}[A-Za-z][A-Za-z'’-]+", text):
                found.append(f'{path}: "{m.group(0)[:60]}"')
        elif isinstance(x, list):
            for i, v in enumerate(x):
                walk(v, f'{path}[{i}]')
        elif isinstance(x, dict):
            for k, v in x.items():
                if k not in SKIP and k not in ('columns',):
                    walk(v, f'{path}.{k}')
    walk({k: v for k, v in topic.items() if k != 'code_examples'}, topic['id'])
    for ex in topic.get('code_examples', []):
        walk({k: v for k, v in ex.items() if k in ('title', 'intro', 'explanation', 'walkthrough')}, f"{topic['id']}.{ex['id']}")
    return found


def check():
    errors = []
    for code in DEEPENED:
        _, zh, _ = editions(code)
        for tid, r in ratios(code):
            if r < FLOOR:
                errors.append(f'{code}/{tid}: Chinese is {r:.2f} of the English (floor {FLOOR})')
        for t in zh['topics']:
            errors += [f'{code}/{e}' for e in english_left(t)]
    if errors:
        raise SystemExit('\n'.join(errors))
    means = {code: round(sum(r for _, r in ratios(code)) / len(ratios(code)), 2) for code in DEEPENED}
    print(f'PASS: every chapter of {", ".join(DEEPENED)} is at least {FLOOR} of its English in Chinese; means {means}')


def report(codes):
    for code in codes or DEEPENED + ('COMP2017', 'INFO1113'):
        rs = ratios(code)
        thin = [f'{t} {r:.2f}' for t, r in rs if r < FLOOR]
        print(f'{code}: mean {sum(r for _, r in rs) / len(rs):.2f}, {len(thin)} of {len(rs)} below {FLOOR}')
        for line in thin:
            print('   ', line)


PROGRAM_FIELDS = ('id', 'code', 'output', 'language')


def show(code, tid):
    en, zh, _ = editions(code)
    t = next(t for t in en['topics'] if t['id'] == tid)
    z = next(t for t in zh['topics'] if t['id'] == tid)
    strip = lambda topic: {**topic, 'code_examples': [{k: v for k, v in ex.items() if k not in ('code', 'output')} for ex in topic.get('code_examples', [])]}
    print(f'=== ENGLISH {code}/{tid} (prose {prose_len(t)} chars; translate all of it) ===')
    print(json.dumps(strip(t), ensure_ascii=False, indent=1))
    print(f'=== CURRENT CHINESE (prose {prose_len(z)} chars, ratio {prose_len(z) / prose_len(t):.2f}; compressed, rewrite in full) ===')
    print(json.dumps(strip(z), ensure_ascii=False, indent=1))
    for ex in t.get('code_examples', []):
        print(f"=== PROGRAM {ex['id']} ({ex.get('language', 'python')}), read-only, identical in both editions ===")
        print(ex['code'])
        print('--- output ---')
        print(ex['output'])


def apply(code, tid, path):
    en, zh, zh_path = editions(code)
    t = next(t for t in en['topics'] if t['id'] == tid)
    i = next(i for i, x in enumerate(zh['topics']) if x['id'] == tid)
    old = zh['topics'][i]
    new = json.loads(Path(path).read_text())
    problems = []
    new['id'] = tid
    if set(new) != set(t):
        problems.append(f'keys differ from the English chapter: missing {sorted(set(t) - set(new))}, extra {sorted(set(new) - set(t))}')
    for key in ('glossary', 'guided_questions', 'instructor_notes', 'worked_problems', 'code_examples'):
        if len(new.get(key, [])) != len(t.get(key, [])):
            problems.append(f'{key}: {len(new.get(key, []))} entries, English has {len(t.get(key, []))}')
    merged_examples = []
    for a, b, o in zip(t.get('code_examples', []), new.get('code_examples', []), old.get('code_examples', [])):
        if b.get('id') != a['id']:
            problems.append(f"code example order: {b.get('id')} where English has {a['id']}")
        for k in ('code', 'output'):
            if k in b and b[k] != a[k]:
                problems.append(f"{a['id']}: {k} must stay identical to the English edition")
        if set(b) - {'code', 'output'} != set(a) - {'code', 'output'}:
            problems.append(f"{a['id']}: fields {sorted(set(b) - {'code', 'output'})}, English has {sorted(set(a) - {'code', 'output'})}")
        if len(b.get('walkthrough', [])) != len(a.get('walkthrough', [])):
            problems.append(f"{a['id']}: walkthrough has {len(b.get('walkthrough', []))} steps, English has {len(a['walkthrough'])}")
        if a.get('trace'):
            tr = b.get('trace') or {}
            if len(tr.get('columns', [])) != len(a['trace']['columns']) or len(tr.get('rows', [])) != len(a['trace']['rows']) or any(len(r) != len(a['trace']['columns']) for r in tr.get('rows', [])):
                problems.append(f"{a['id']}: trace shape differs from the English")
        if len(b.get('syntax_notes', [])) != len(a.get('syntax_notes', [])):
            problems.append(f"{a['id']}: syntax_notes count differs")
        merged_examples.append({**b, 'id': a['id'], 'code': a['code'], 'output': a['output'], 'language': a.get('language', o.get('language'))} if 'language' in a else {**b, 'id': a['id'], 'code': a['code'], 'output': a['output']})
    for a, b in zip(t.get('worked_problems', []), new.get('worked_problems', [])):
        if len(b.get('steps', [])) != len(a.get('steps', [])):
            problems.append(f"worked problem '{a['title'][:30]}': {len(b.get('steps', []))} steps, English has {len(a['steps'])}")
    for key in ('title', 'story', 'principle', 'symbols', 'example', 'pitfall'):
        if not HAN.search(str(new.get(key, ''))):
            problems.append(f'{key} has no Chinese')
    if t.get('code_examples'):
        new['code_examples'] = merged_examples
    new = {k: new[k] for k in t if k in new}
    r = prose_len(new) / max(1, prose_len(t))
    left = english_left(new)
    if left:
        problems += ['untranslated English: ' + x for x in left[:8]]
    if r < FLOOR:
        problems.append(f'Chinese is {r:.2f} of the English; a full translation of every sentence is about 0.40 to 0.45. Translate what was left out, do not pad')
    if problems:
        raise SystemExit(f'{code}/{tid} not applied:\n  - ' + '\n  - '.join(problems))
    zh['topics'][i] = new
    zh_path.write_text(json.dumps(zh, ensure_ascii=False, indent=2) + '\n')
    print(f'applied {code}/{tid}: ratio {prose_len(old) / prose_len(t):.2f} -> {r:.2f}')


if __name__ == '__main__':
    cmd, *args = sys.argv[1:] or ['report']
    {'report': lambda: report(args), 'check': check, 'show': lambda: show(*args), 'apply': lambda: apply(*args)}[cmd]()
