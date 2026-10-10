"""Connect guided cases to their existing lessons in both language editions."""
from html import escape as E
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GROUPS = json.loads((ROOT / 'content/learning-extensions.json').read_text())['groups']
LABEL = {'en': 'Guided extensions', 'zh': '继续深入：完整案例'}
INTRO = {
    'en': 'Read the linked lesson first. Then follow the story, predict the output, run the complete program and check the explanation. Each case adds one practical challenge.',
    'zh': '先读对应章节，再跟着故事预测输出、运行完整程序、核对解释。每个案例都在原有概念上增加一个实际问题。',
}


def group_for(document):
    return document['code'] if document['code'] in GROUPS else 'AI-' + document['code']


def anchor(case):
    return 'lab-' + case['topic'] + '-' + case['example']


def extension_link(document, lang='en'):
    if group_for(document) not in GROUPS:
        return ''
    return f'<a class="toc-group" href="#extensions">{LABEL[lang]}</a>'


def extension_html(document, lang='en'):
    cases = GROUPS.get(group_for(document), [])
    if not cases:
        return ''
    cards = []
    topics = {t['id']: t for t in document['topics']}
    for i, case in enumerate(cases, 1):
        lesson = topics[case['topic']]['title']
        if isinstance(lesson, dict):
            lesson = lesson[lang]
        read = 'Read the lesson' if lang == 'en' else '先读对应章节'
        cards.append(f'''<li><a class="route-node" href="#{anchor(case)}"><span class="route-step">{i:02d} <span aria-hidden="true">↗</span></span><h3>{E(case['title'][lang])}</h3><p>{E(case['goal'][lang])}</p><span class="route-count">{'Story · Code · Reasoning' if lang == 'en' else '故事 · 代码 · 推理'}</span></a><a class="extension-prerequisite" href="#{case['topic']}">{read}: {E(lesson)}</a></li>''')
    return f'''<section class="learning-route extension-route" id="extensions" data-reading-id="extensions" aria-labelledby="extensions-title"><div class="route-heading"><div><span class="eyebrow">LEON / FROM IDEAS TO IMPLEMENTATION</span><h2 id="extensions-title">{LABEL[lang]}</h2></div><p>{INTRO[lang]}</p></div><ol class="route-flow">{''.join(cards)}</ol></section>'''


def extension_markdown(document, lang='en'):
    cases = GROUPS.get(group_for(document), [])
    if not cases:
        return ''
    entries = [f'<a id="extensions"></a>\n\n## {LABEL[lang]}', INTRO[lang]]
    entries.extend(f"{i}. [{case['title'][lang]}](#{anchor(case)}) — {case['goal'][lang]}" for i, case in enumerate(cases, 1))
    return '\n\n'.join(entries)


def home_extensions(courses, guides):
    entries = []
    for document in courses + guides:
        group = group_for(document)
        cases = GROUPS.get(group, [])
        if not cases:
            continue
        base = ('courses/' + document['code'].lower()) if group == document['code'] else ('ai/' + document['id'])
        en = base + ('.html' if group == document['code'] else '.en.html')
        zh = base + '.zh.html'
        entries.append(f'<li><strong>{E(group)}</strong><span>{len(cases)} guided cases</span><a href="{en}#extensions" lang="en">EN ↗</a><a href="{zh}#extensions" lang="zh">ZH ↗</a></li>')
    count = sum(len(cases) for cases in GROUPS.values())
    return f'''<section class="extension-summary" id="extensions-library" aria-labelledby="extensions-library-title"><span class="eyebrow">CONTINUE YOUR LEARNING</span><h3 id="extensions-library-title">From an idea to a working solution.</h3><p>{count} additional guided cases connect the existing lessons to practical decisions. Build safer C programs, test algorithm choices, work through proofs, and check AI results. Every case includes a story, complete code, expected output and step-by-step reasoning in English and Chinese.</p><ul>{''.join(entries)}</ul></section>'''
