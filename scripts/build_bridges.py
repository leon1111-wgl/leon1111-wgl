#!/usr/bin/env python3
"""Write the first-steps and writing-by-hand guides (site/bridges/) from content/bridges/*.json."""
from html import escape as E
from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from teaching import asset_version, code_html, paragraphs, RUNNABLE
from palette import COURSE_COLORS
import seo

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'content' / 'bridges'
OUT = ROOT / 'site' / 'bridges'
RUN_NAMES = {'python': 'Python 3', 'java': 'Java 8+', 'c': 'C11'}
WORDS = {
    'en': dict(needs='What you need first', setup='Set up your computer', setup_note='Optional at first: the examples below also run on this page.', verify='Check it worked', expect='You should see', errors='If you see an error', goal='Goal', terms='New words', example='Worked example', walk='Step by step', output='Expected output', fold_output='Predict the output first, then show it', mistakes='Common mistakes', wrong='Wrong', right='Right', check='Check yourself', fold='Try it first, then show the answer', next='What next', contents='In this guide', hub='Leon Learn', copy='Copy code', unofficial='Independent study notes, not official course material.', home='All courses'),
    'zh': dict(needs='开始前需要什么', setup='准备你的电脑', setup_note='一开始可以跳过：下面的例子在这个页面上就能运行。', verify='检查是否成功', expect='你应该看到', errors='如果看到报错', goal='学完你能', terms='新词', example='完整例子', walk='逐步讲解', output='预期输出', fold_output='先预测输出，再看结果', mistakes='常见错误', wrong='错误写法', right='正确写法', check='检查自己', fold='先自己做，再看答案', next='接下来', contents='本篇目录', hub='Leon 学习', copy='复制代码', unofficial='独立整理的学习笔记，不是官方课程材料。', home='全部课程'),
}


def L(value, lang):
    return value[lang] if isinstance(value, dict) else value


def page_name(guide, lang):
    return f'{guide["id"]}.zh.html' if lang == 'zh' else f'{guide["id"]}.html'


def example_key(guide, lesson):
    return f'bridges/{guide["id"]}/{lesson["id"]}'


def walk_html(rows):
    """Runs of `a | b | c` lines are dry-run tables; everything else stays a numbered step."""
    out, table = [], []

    def flush():
        if table:
            head, *rest = table
            out.append('<div class="trace-wrap" tabindex="0"><table class="trace-table"><thead><tr>' + ''.join(f'<th scope="col">{E(c)}</th>' for c in head) + '</tr></thead><tbody>'
                       + ''.join('<tr>' + ''.join(f'<td>{E(c)}</td>' for c in r) + '</tr>' for r in rest) + '</tbody></table></div>')
            table.clear()
    steps = []

    def flush_steps():
        if steps:
            out.append('<ol class="execution-steps">' + ''.join(f'<li>{paragraphs(x)}</li>' for x in steps) + '</ol>')
            steps.clear()
    for row in rows:
        if ' | ' in row:
            flush_steps()
            table.append([c.strip() for c in row.split(' | ')])
        else:
            flush()
            steps.append(row)
    flush()
    flush_steps()
    return ''.join(out)


def example_html(guide, lesson, lang):
    example = lesson.get('example')
    if not example:
        return ''
    w = WORDS[lang]
    language = example['language']
    key = example_key(guide, lesson)
    code_id = f'code-{lesson["id"]}'
    run = f' data-run="{language}"' if key in RUNNABLE else ''
    hidden = (f'<div class="output-block"><h4>{w["output"]}</h4><pre class="code code-output">{E(example["output"])}</pre></div>'
              + (f'<h4>{w["walk"]}</h4>{walk_html(example.get("walk", {}).get(lang, []))}' if example.get('walk') else ''))
    return (f'<section class="code-example"{run}><h3>{w["example"]}</h3><div class="code-actions"><span>{RUN_NAMES[language]}</span>'
            f'<button type="button" data-copy-code="{code_id}">{w["copy"]}</button></div>{code_html(example["code"], language, code_id)}'
            f'<details class="try-first"><summary>{w["fold_output"]}</summary><div class="try-body">{hidden}</div></details></section>')


def lesson_html(guide, lesson, lang, index):
    w = WORDS[lang]
    terms = ''.join(f'<div><dt>{E(L(t["term"], lang))}</dt><dd>{E(L(t["meaning"], lang))}</dd></div>' for t in lesson.get('terms', []))
    mistakes = ''.join(f'<article class="mistake"><div><h5>{w["wrong"]}</h5><pre class="code">{E(m["wrong"])}</pre></div>{paragraphs(L(m["why"], lang))}<div><h5>{w["right"]}</h5><pre class="code">{E(m["right"])}</pre></div></article>' for m in lesson.get('mistakes', []))
    checks = ''.join(f'<li><p>{E(L(c["q"], lang))}</p><details class="try-first"><summary>{w["fold"]}</summary><div class="try-body">{paragraphs(L(c["a"], lang))}</div></details></li>' for c in lesson.get('check', []))
    return (f'<article class="topic bridge-lesson" id="{E(lesson["id"])}"><div class="topic-head"><span class="topic-number">{index:02d}</span></div><h2>{E(L(lesson["title"], lang))}</h2>'
            f'<p class="bridge-goal"><b>{w["goal"]}</b> {E(L(lesson["goal"], lang))}</p>{paragraphs(L(lesson["plain"], lang))}'
            + (f'<section class="glossary"><h3>{w["terms"]}</h3><dl>{terms}</dl></section>' if terms else '')
            + example_html(guide, lesson, lang)
            + (f'<section class="bridge-mistakes"><h3>{w["mistakes"]}</h3>{mistakes}</section>' if mistakes else '')
            + (f'<section class="guided"><h3>{w["check"]}</h3><ol>{checks}</ol></section>' if checks else '')
            + '</article>')


def setup_html(guide, lang):
    setup = guide.get('setup')
    if not setup:
        return ''
    w = WORDS[lang]
    systems = ''
    for s in setup['systems']:
        steps = ''.join(f'<li>{paragraphs(L(x, lang))}</li>' for x in s['steps'])
        systems += (f'<details class="setup-system"><summary>{E(L(s["name"], lang))}</summary><ol>{steps}</ol><p><b>{w["verify"]}</b></p><pre class="code">{E(s["verify"])}</pre>'
                    f'<p><b>{w["expect"]}</b> {E(L(s["expect"], lang))}</p></details>')
    errors = ''.join(f'<li><code>{E(e["symptom"])}</code>{paragraphs(L(e["fix"], lang))}</li>' for e in setup.get('errors', []))
    return (f'<section class="bridge-setup" id="setup"><h2>{w["setup"]}</h2><p class="muted-note">{w["setup_note"]}</p>{paragraphs(L(setup["intro"], lang))}{systems}'
            + (f'<h3>{w["errors"]}</h3><ul class="setup-errors">{errors}</ul>' if errors else '') + '</section>')


def render(guide, lang):
    w = WORDS[lang]
    iso = 'zh-Hans' if lang == 'zh' else 'en'
    color = COURSE_COLORS.get(guide.get('course'), '#4c9bff')
    title, summary = L(guide['title'], lang), L(guide['summary'], lang)
    alternates = {l: 'bridges/' + page_name(guide, l) for l in ('en', 'zh')}
    tags = seo.head(alternates[lang], title, summary, lang, alternates, data=seo.course_data(title, summary, alternates[lang], lang, kind='LearningResource'))
    switch = ''.join(f'<a href="{page_name(guide, l)}" lang="{l}" hreflang="{l}" data-language="{l}"' + (' aria-current="page"' if l == lang else '') + f'>{name}</a>' for l, name in [('en', 'EN'), ('zh', '中文')])
    needs = ''.join(f'<li>{E(L(x, lang))}</li>' for x in guide.get('needs', []))
    toc = ''.join(f'<li><a href="#{E(x["id"])}">{E(L(x["title"], lang))}</a></li>' for x in guide['lessons'])
    next_item = guide.get('next')
    next_html = ''
    if next_item:
        href = next_item.get('hrefZh', next_item['href']) if lang == 'zh' else next_item['href']
        next_html = f'<section class="bridge-next"><h2>{w["next"]}</h2><p><a class="button primary" href="../{E(href)}">{E(L(next_item["text"], lang))} →</a></p></section>'
    lessons = ''.join(lesson_html(guide, x, lang, i) for i, x in enumerate(guide['lessons'], 1))
    return f'''<!doctype html><html lang="{iso}" data-theme="dark"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{E(summary)}"><meta name="theme-color" content="#000000"><title>{E(title)} | Leon</title>{tags}<link rel="icon" href="../assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="../assets/style.css?v={asset_version("style.css")}"><link rel="stylesheet" href="../assets/reader.css?v={asset_version("reader.css")}"><script defer src="../assets/app.js?v={asset_version("app.js")}"></script><script defer src="../assets/run-ui.js?v={asset_version("run-ui.js")}"></script></head><body class="field-guide foundation-guide reader bridge-guide" style="--course:{color}"><a class="skip" href="#main">{"跳到正文" if lang == "zh" else "Skip to content"}</a><header class="topbar"><div class="wrap"><a class="brand" href="../learn/"><span class="monogram">LW</span> {w["hub"]}</a><nav class="language-switch" aria-label="Language">{switch}</nav><button class="theme-button" type="button" data-theme-toggle>☼</button></div></header><main id="main" class="wrap"><header class="course-hero" id="top"><div class="reader-tags"><a class="code-chip" href="../learn/#/courses">← {w["home"]}</a></div><h1>{E(title)}</h1><p>{E(summary)}</p></header><div class="course-body bridge-body">{f'<section class="overview"><h2>{w["needs"]}</h2><ul>{needs}</ul></section>' if needs else ''}<nav class="bridge-toc" aria-label="{w["contents"]}"><h2>{w["contents"]}</h2><ol>{toc}</ol></nav>{setup_html(guide, lang)}{lessons}{next_html}<p class="muted-note">{w["unofficial"]}</p></div></main></body></html>
'''


def guides():
    return [json.loads(p.read_text()) for p in sorted(SOURCE.glob('*.json'))]


def build():
    OUT.mkdir(exist_ok=True)
    found = guides()
    examples = []
    for guide in found:
        for lang in ('en', 'zh'):
            (OUT / page_name(guide, lang)).write_text(render(guide, lang))
        for lesson in guide['lessons']:
            if lesson.get('example'):
                e = lesson['example']
                examples.append({'path': example_key(guide, lesson), 'language': e['language'], 'code': e['code'], 'output': e['output']})
    (OUT / 'examples.json').write_text(json.dumps(examples, ensure_ascii=False, separators=(',', ':')))
    print(f'bridges: {len(found)} guides, {len(examples)} examples')


if __name__ == '__main__':
    build()
