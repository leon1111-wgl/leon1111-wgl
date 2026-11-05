#!/usr/bin/env python3
"""Write site/learn/data/<course>.json: everything the practice and review views use for one course.

Derived from the lessons, with no new wording: review cards (chapter checks and guided questions), predict-the-output drills
(every short program, with its exact verified output) and worked problems marked step by step. Authored questions, mock papers
and labs come from content/practice/<course>.json (schema in content/practice/SCHEMA.md).
"""
from pathlib import Path
import json
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from teaching import example_path, RUNNABLE

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / 'content'
OUT = ROOT / 'site' / 'learn' / 'data'
COURSES = ['INFO1113', 'COMP2017', 'COMP2123', 'COMP2022', 'COMP3308']
GUIDES = {'start': ('primer.json', 'AI-START'), 'ml': ('paths/ml.json', 'AI-ML'), 'dl': ('paths/dl.json', 'AI-DL'),
          'vision': ('paths/vision.json', 'AI-CV'), 'multimodal': ('paths/multimodal.json', 'AI-MM')}
MAX_LINES = 14
# A guided question that leans on the chapter's example cannot be answered alone in a review queue.
NEEDS_CONTEXT = re.compile(r'\b(?:the|this|that|these|those)\s+(?:example|story|code|program|trace|table|output|tree|graph|figure|diagram|run|case|loop|line|function|grid|list|array|machine|grammar|string|formula|calculation|setup|plan|design|model|query|result)\b|\b(?:here|above|below|earlier|in step|step \d)\b|^(?:why|what|how|does|is|can|would)\b.*\b(?:it|its|they|their)\b.{0,12}\?$|这个例子|这段|该例|例子中|上面|下面|这里|本例|这张|这棵|这条|这组|此处', re.I)
MAX_CODE = 80


# Review cards a reader could not answer alone a week later, reviewed by hand: they lean on a chapter's own example.
EXCLUDED = set(json.loads((CONTENT / 'card-exclude.json').read_text())) if (CONTENT / 'card-exclude.json').exists() else set()


def both(en, zh):
    return {'en': en, 'zh': zh}


def text(value, lang):
    return value[lang] if isinstance(value, dict) else value


def predict_item(topic, example, group, zh_example=None):
    """A drill only if a person could sensibly work the output out on paper."""
    output = example['output']
    code = example['code']
    if len(output.splitlines()) > MAX_LINES or len(output) > 600 or len(code.splitlines()) > MAX_CODE or not output.strip():
        return None
    language = example.get('language', 'python')
    path = example_path(group, topic, example)
    zh = zh_example or example
    item = {'id': 'p-' + topic['id'] + '-' + example['id'], 'kind': 'predict', 'topic': topic['id'], 'language': language,
            'title': both(text(example['title'], 'en'), text(zh['title'], 'zh')),
            'intro': both(text(example['intro'], 'en'), text(zh['intro'], 'zh')),
            'code': code, 'output': output, 'marks': min(max(len(output.splitlines()), 1), 6),
            'walk': both([text(x, 'en') for x in example.get('walkthrough', [])], [text(x, 'zh') for x in zh.get('walkthrough', [])])}
    if example.get('trace'):
        trace, ztrace = example['trace'], zh.get('trace') or example['trace']
        item['trace'] = {'columns': both([text(x, 'en') for x in trace['columns']], [text(x, 'zh') for x in ztrace['columns']]),
                         'rows': both([[text(c, 'en') for c in r] for r in trace['rows']], [[text(c, 'zh') for c in r] for r in ztrace['rows']])}
    if path in RUNNABLE:
        item['run'] = True
    return item


def from_course(code):
    en = json.loads((CONTENT / f'{code}.json').read_text())
    zh = json.loads((CONTENT / 'translations' / f'{code}.zh.json').read_text())
    ztopics = {t['id']: t for t in zh['topics']}
    cards, predict, worked = [], [], []
    for topic in en['topics']:
        z = ztopics[topic['id']]
        cards.append({'id': f'c-{topic["id"]}-check', 'topic': topic['id'], 'q': both(topic['check']['question'], z['check']['question']),
                      'a': both(topic['check']['answer'], z['check']['answer'])})
        for i, (q, zq) in enumerate(zip(topic.get('guided_questions', []), z.get('guided_questions', []))):
            if NEEDS_CONTEXT.search(q['question']) or NEEDS_CONTEXT.search(zq['question']):
                continue
            cards.append({'id': f'c-{topic["id"]}-{i}', 'topic': topic['id'], 'q': both(q['question'], zq['question']), 'a': both(q['answer'], zq['answer'])})
        zex = {x['id']: x for x in z.get('code_examples', [])}
        for example in topic.get('code_examples', []):
            item = predict_item(topic, example, code, zex.get(example['id']))
            if item:
                predict.append(item)
        for i, (p, zp) in enumerate(zip(topic.get('worked_problems', []), z.get('worked_problems', []))):
            worked.append(worked_item(topic['id'], i, p, zp))
    return cards, predict, worked


def worked_item(topic, i, p, zp):
    return {'id': f'w-{topic}-{i}', 'kind': 'worked', 'topic': topic, 'title': both(p['title'], zp['title']), 'question': both(p['question'], zp['question']),
            'strategy': both(p['strategy'], zp['strategy']), 'steps': both(p['steps'], zp['steps']), 'answer': both(p['answer'], zp['answer']),
            'sanity': both(p['sanity_check'], zp['sanity_check']), 'marks': len(p['steps'])}


def from_guide(name):
    file, group = GUIDES[name]
    g = json.loads((CONTENT / file).read_text())
    cards, predict = [], []
    for topic in g['topics']:
        for i, q in enumerate(topic.get('guided_questions', [])):
            if NEEDS_CONTEXT.search(q['question']['en']) or NEEDS_CONTEXT.search(q['question']['zh']):
                continue
            cards.append({'id': f'c-{topic["id"]}-{i}', 'topic': topic['id'], 'q': q['question'], 'a': q['answer']})
        for example in topic.get('code_examples', []):
            item = predict_item(topic, example, group)
            if item:
                predict.append(item)
    return cards, predict, []


STOP = set('if for while switch return sizeof int char void main print printf len range str list dict set string class new this'.split())


def keywords():
    """Words a chapter teaches but may not name in its title: glossary terms and the functions its programs call."""
    out = {}
    sources = [(c.lower(), json.loads((CONTENT / f'{c}.json').read_text()), json.loads((CONTENT / 'translations' / f'{c}.zh.json').read_text())) for c in COURSES]
    sources += [(g, json.loads((CONTENT / GUIDES[g][0]).read_text()), None) for g in GUIDES]
    for cid, en, zh in sources:
        ztopics = {t['id']: t for t in zh['topics']} if zh else {}
        chapters = out.setdefault(cid, {})
        for topic in en['topics']:
            words = []
            for term in topic.get('glossary', []) + ztopics.get(topic['id'], {}).get('glossary', []):
                name = term['term']
                words.extend(name.values() if isinstance(name, dict) else [name])
            calls = set()
            for example in topic.get('code_examples', []):
                calls.update(re.findall(r'\b([A-Za-z_][A-Za-z0-9_]{2,})\s*\(', example['code']))
                calls.update(re.findall(r'#include\s*<([a-z0-9_./]+)>', example['code']))
            words.extend(sorted(x for x in calls if x not in STOP)[:40])
            chapters[topic['id']] = ' '.join(words)
    return out


def term_lists():
    """Every glossary entry in a course, for the tap-to-define words on its reading pages."""
    sources = [(c.lower(), json.loads((CONTENT / f'{c}.json').read_text()), json.loads((CONTENT / 'translations' / f'{c}.zh.json').read_text())) for c in COURSES]
    sources += [(g, json.loads((CONTENT / GUIDES[g][0]).read_text()), None) for g in GUIDES]
    extra_dir = CONTENT / 'terms'
    for cid, en, zh in sources:
        out = {'en': {}, 'zh': {}}
        ztopics = {t['id']: t for t in zh['topics']} if zh else {}
        for topic in en['topics']:
            pairs = zip(topic.get('glossary', []), ztopics.get(topic['id'], {}).get('glossary', [])) if zh else ((g, g) for g in topic.get('glossary', []))
            for a, b in pairs:
                out['en'].setdefault(text(a['term'], 'en'), text(a['meaning'], 'en'))
                out['zh'].setdefault(text(b['term'], 'zh'), text(b['meaning'], 'zh'))
        extra = extra_dir / f'{cid}.json'
        if extra.exists():
            for item in json.loads(extra.read_text()):
                out['en'].setdefault(item['term']['en'], item['meaning']['en'])
                out['zh'].setdefault(item['term']['zh'], item['meaning']['zh'])
        (OUT / f'terms-{cid}.json').write_text(json.dumps(out, ensure_ascii=False, separators=(',', ':')))


def labs_for(cid):
    """Labs for this course, with the output CI captured from really running them."""
    found = []
    root = CONTENT / 'labs'
    for folder in sorted(root.iterdir()) if root.exists() else []:
        if not (folder / 'lab.json').exists():
            continue
        lab = json.loads((folder / 'lab.json').read_text())
        if lab['course'] != cid:
            continue
        captured = json.loads((folder / 'captured.json').read_text()) if (folder / 'captured.json').exists() else {}
        for i, step in enumerate(lab['steps']):
            text = captured.get(str(i))
            if text is not None:
                lines = text.rstrip('\n').split('\n')
                limit = step.get('lines', 40)
                step['output'] = '\n'.join(lines[:limit]) + ('\n…' if len(lines) > limit else '')
            step.pop('contains', None)
        lab['files'] = [{'path': name, 'text': (folder / 'files' / name).read_text()} for name in lab.get('show', [])]
        found.append(lab)
    return found


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'keywords.json').write_text(json.dumps(keywords(), ensure_ascii=False, separators=(',', ':')))
    term_lists()
    summary = {}
    practice = CONTENT / 'practice'
    # the Python handbook keeps its own exercises; its practice here is authored only
    for cid, source in [(c.lower(), lambda c=c: from_course(c)) for c in COURSES] + [(g, lambda g=g: from_guide(g)) for g in GUIDES] + [('python', lambda: ([], [], []))]:
        cards, predict, worked = source()
        cards = [c for c in cards if f'{cid}/{c["id"]}' not in EXCLUDED]
        pack = json.loads((practice / f'{cid}.json').read_text()) if (practice / f'{cid}.json').exists() else {}
        data = {'course': cid, 'cards': cards, 'questions': predict + worked + pack.get('questions', []), 'papers': pack.get('papers', []), 'labs': labs_for(cid)}
        (OUT / f'{cid}.json').write_text(json.dumps(data, ensure_ascii=False, separators=(',', ':')))
        kinds = {}
        for q in data['questions']:
            kinds[q['kind']] = kinds.get(q['kind'], 0) + 1
        summary[cid] = {'cards': len(cards), 'kinds': kinds, 'papers': len(data['papers']), 'labs': len(data['labs'])}
    (OUT / 'summary.json').write_text(json.dumps(summary, separators=(',', ':')))
    print('study data:', {k: (v['cards'], sum(v['kinds'].values()), v['papers']) for k, v in summary.items()})
    return summary


if __name__ == '__main__':
    build()
