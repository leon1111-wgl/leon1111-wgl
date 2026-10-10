#!/usr/bin/env python3
"""Check guided-case targets, complete translations and exported entry points."""
from html import escape
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
AI = {'AI-ML': 'ml', 'AI-DL': 'dl', 'AI-CV': 'vision', 'AI-MM': 'multimodal'}


def validate_extensions():
    manifest = json.loads((ROOT / 'content/learning-extensions.json').read_text())
    errors, count = [], 0

    def check(condition, message):
        if not condition:
            errors.append(message)

    def bilingual(value, label):
        valid = isinstance(value, dict) and set(value) == {'en', 'zh'} and all(isinstance(v, str) and v.strip() for v in value.values())
        check(valid, label + ': missing translation')
        if valid:
            check(not re.search('[\u4e00-\u9fff]', value['en']), label + ': Chinese in English edition')
            check(bool(re.search('[\u4e00-\u9fff]', value['zh'])), label + ': Chinese translation absent')

    for group, cases in manifest['groups'].items():
        is_ai = group in AI
        paths = [ROOT / 'content/paths' / (AI[group] + '.json')] if is_ai else [ROOT / 'content' / (group + '.json'), ROOT / 'content/translations' / (group + '.zh.json')]
        docs = [json.loads(p.read_text()) for p in paths]
        keys = [(case['topic'], case['example']) for case in cases]
        check(len(keys) == len(set(keys)), group + ': duplicate case')
        for case in cases:
            count += 1
            label = group + '/' + case['example']
            for field in ('title', 'goal'):
                bilingual(case[field], label + '/' + field)
            selected = []
            for doc in docs:
                topic = next((t for t in doc['topics'] if t['id'] == case['topic']), None)
                example = next((e for e in topic.get('code_examples', []) if e['id'] == case['example']), None) if topic else None
                check(example is not None, label + ': missing target example')
                if example:
                    selected.append(example)
                    check(len(example.get('walkthrough', [])) >= 3, label + ': insufficient execution guidance')
                    if is_ai:
                        for field in ('title', 'intro', 'explanation'):
                            bilingual(example[field], label + '/' + field)
                        for step in example['walkthrough']:
                            bilingual(step, label + '/walkthrough')
            if not is_ai and len(selected) == 2:
                for key in ('id', 'language', 'code', 'output'):
                    check(selected[0][key] == selected[1][key], label + ': source/output differs between editions')
            anchor = 'lab-' + case['topic'] + '-' + case['example']
            for lang in ('en', 'zh'):
                page = 'ai/' + AI[group] + '.' + lang + '.html' if is_ai else 'courses/' + group.lower() + ('.zh' if lang == 'zh' else '') + '.html'
                note = group + ('.' + lang if is_ai else '.zh' if lang == 'zh' else '') + '.md'
                html = (ROOT / 'site' / page).read_text()
                check('href="#' + anchor + '"' in html and 'id="' + anchor + '"' in html, label + ': broken rendered case link in ' + lang)
                check(escape(case['title'][lang]) in html, label + ': missing case title in ' + lang)
                check(html.index('id="extensions"') < html.index('class="course-layout"'), label + ': case route is too late')
                for directory in ('notes', 'site/notes'):
                    text = (ROOT / directory / note).read_text()
                    check('](#' + anchor + ')' in text and 'id="' + anchor + '"' in text, label + ': broken downloaded case link')
    return errors, count


if __name__ == '__main__':
    errors, count = validate_extensions()
    if errors:
        raise SystemExit('\n'.join(errors))
    print(f'PASS: {count} guided cases, EN/ZH scaffolds, shared source and HTML/Markdown entry points.')
