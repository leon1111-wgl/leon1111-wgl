"""Render both editions of the five foundational courses without changing old URLs."""
from pathlib import Path
from html import escape as E
import json
import re
from teaching import paragraphs as para, asset_version, glossary_html, teaching_html, teaching_markdown, course_reading_tools, code_html, run_notes
from roadmaps import roadmap_html, roadmap_markdown, build_roadmap
from course_path import path_html, path_md, coach, coach_md
ROOT=Path(__file__).resolve().parents[1];SITE=ROOT/'site'
LABELS={
'en':dict(home='Home',learning='Learning',contents='IN THIS COURSE',map='Connected knowledge framework',mapintro='The stages show the learning order. Select any topic to read its story, method and examples.',before='Before you start',outcomes='What you will learn',story='01 / The story',principle='02 / The principle',formula='03 / The formula, unpacked',example='04 / A first worked example',pitfall='Watch out',check='Check your understanding',back='Back to the knowledge framework',references='Continue exploring',notes='Download English notes',cheat='One-page cheatsheet · EN',cheatweb='Read the reference in this language',scope='Original stories, explanations and worked problems by Leon. Course codes identify independent study paths. The linked references belong to their authors.',footer='Research, ideas & learning in public.',reference='Core concepts, formulas and conditions at a glance.',print='Print this view',switch='Reading language',overview='Prepare for the journey',skip='Skip to content'),
'zh':dict(home='首页',learning='学习资料',contents='本课程目录',map='把知识连接起来',mapintro='按阶段循序渐进。也可以点击任一主题，阅读故事、方法与例子。',before='开始前需要了解',outcomes='你将学到什么',story='01 / 从一个故事开始',principle='02 / 理解原理',formula='03 / 逐项读懂公式',example='04 / 先看一个完整例子',pitfall='注意这个边界',check='检查自己的理解',back='返回知识框架',references='继续探索',notes='下载中文讲义',cheat='一页纸速查表 · 英文 PDF',cheatweb='阅读中文速查表',scope='故事、概念讲解和推导例题由 Leon 原创编写。课程代号标识独立学习路径。参考资料属于各自作者。',footer='分享研究、想法与学习。',reference='集中回顾核心概念、公式和适用条件。',print='打印当前页面',switch='阅读语言',overview='开始学习之前',skip='跳到正文')}


def suffix(lang):return '.zh.html' if lang=='zh' else '.html'
def note_name(c,lang):return c['code']+('.zh' if lang=='zh' else '')+'.md'


def illustration_notes(topic, lang):
    """Give named Java illustrations their own correct file and launch command."""
    if topic.get('language') != 'java':
        return ''
    match = re.search(r'public\s+class\s+(\w+)', topic.get('code', ''))
    if not match:
        return ''
    name = match.group(1)
    instruction = (f'将这个短例子另存为 {name}.java，放在单独文件夹中。运行：'
                   if lang == 'zh' else
                   f'Save this short illustration as {name}.java in its own folder. Run:')
    return instruction + f'\n\njavac -encoding UTF-8 {name}.java\njava -ea {name}'


def shell(c,lang,body,cheat=False):
    lab=LABELS[lang];slug=c['code'].lower();iso='zh-Hans' if lang=='zh' else 'en'
    links=''.join(f'<a href="{slug}{suffix(l)}" lang="{l}" hreflang="{l}" data-language="{l}"'+(' aria-current="page"' if l==lang else '')+f'>{name}</a>' for l,name in [('en','EN'),('zh','中文')])
    return f'''<!doctype html><html lang="{iso}" data-theme="dark"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{E(c['description'])}"><meta name="theme-color" content="#090e17"><meta property="og:title" content="{E(c['title'])}"><meta property="og:description" content="{E(c['description'])}"><meta property="og:type" content="website"><title>{E(c['title'])} | Leon</title><link rel="alternate" hreflang="en" href="{slug}.html"><link rel="alternate" hreflang="zh-Hans" href="{slug}.zh.html"><link rel="icon" href="../assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="../assets/style.css?v={asset_version('style.css')}"><script defer src="../assets/app.js?v={asset_version('app.js')}"></script></head><body class="field-guide foundation-guide"><a class="skip" href="#main">{lab['skip']}</a><header class="topbar"><div class="wrap"><a class="brand" href="../index.html"><span class="monogram">LW</span>Leon<span style="color:var(--accent)">.</span></a><nav aria-label="{lab['contents']}"><a class="guide-home" href="../index.html#learning">{lab['learning']}</a><div class="language-switch" role="navigation" aria-label="{lab['switch']}">{links}</div><button class="theme-button" type="button" data-theme-toggle aria-label="Switch to light theme">☼</button></nav></div></header><main id="main" class="wrap">{body}<footer class="footer"><div><span class="watermark">Leon</span><br>{lab['footer']}</div><a href="../index.html#learning">{lab['learning']} ↑</a><span>© 2026 Leon Wang</span></footer></main></body></html>'''


def edition(c,lang):
    slug=c['code'].lower();lab=LABELS[lang];topics={t['id']:t for t in c['topics']}
    toc=''.join(f'<li><a href="#{t["id"]}">{E(t["title"])}</a></li>' for t in c['topics'])
    stages=''.join(f'<div class="map-stage"><h3>{i+1:02d} / {E(s["title"])}</h3><div class="map-nodes">'+''.join(f'<a href="#{k}">{E(topics[k]["title"])}</a>' for k in s['topics'])+'</div></div>' for i,s in enumerate(c['map']))
    lessons=[]
    for i,t in enumerate(c['topics'],1):
        legacy=code_html(t['code'],t.get('language','text')) if t.get('code') else ''
        if legacy and illustration_notes(t,lang):
            instruction, commands = illustration_notes(t,lang).split('\n\n',1)
            legacy = '<p>'+E(instruction)+'</p>'+legacy+'<pre class="code">'+E(commands)+'</pre>'
        lessons.append(f'''<article class="topic" id="{t['id']}" data-reading-id="{t['id']}"><div class="topic-head"><span class="topic-number">{c['code']} / {i:02d}</span><span class="watermark">Leon</span></div><h2>{E(t['title'])}</h2>{coach(c,t,lang)}<div class="story-principle"><div class="story"><h3>{lab['story']}</h3>{para(t['story'])}</div><div class="principle"><h3>{lab['principle']}</h3>{para(t['principle'])}</div></div>{glossary_html(t,lang)}<div class="formula"><h3>{lab['formula']}</h3><pre>{E(t['formula'])}</pre>{para(t['symbols'])}</div><div class="example"><h3>{lab['example']}</h3>{para(t['example'])}{legacy}</div>{teaching_html(t,c['code'],lang)}<div class="pitfall"><strong>{lab['pitfall']}.</strong> {E(t['pitfall'])}</div><details class="check"><summary>{lab['check']}: {E(t['check']['question'])}</summary>{para(t['check']['answer'])}</details><a class="back-top" href="#framework">↑ {lab['back']}</a></article>''')
    refs=''.join(f'<li><a href="{E(x["url"])}">{E(x["title"])}</a></li>' for x in c.get('references',[]))
    programs=sum(len(t.get('code_examples',[])) for t in c['topics'])
    problems=sum(len(t.get('worked_problems',[])) for t in c['topics'])
    description=('TOPICS · EN + ZH' if lang=='en' else '个主题 · 中英双语')
    if programs:description+=f' · {programs} '+('RUNNABLE PROGRAMS' if lang=='en' else '份可运行代码')
    if problems:description+=f' · {problems} '+('WORKED PROBLEMS' if lang=='en' else '道推导例题')
    extras=('<a class="toc-group" href="#study-plan">'+('Guided study plan' if lang=='en' else '循序学习计划')+'</a><a class="toc-group" href="#projects">'+('Complete projects' if lang=='en' else '完整工程')+'</a>') if c['code']=='COMP2017' else ''
    entry='#study-plan' if c['code']=='COMP2017' else '#framework'
    entry_label=('Start the guided path' if lang=='en' else '开始循序学习') if c['code']=='COMP2017' else lab['map']
    body=f'''<header class="course-hero" id="top"><div class="breadcrumb"><a href="../index.html">{lab['home']}</a><span>/</span><a href="../index.html#learning">{lab['learning']}</a><span>/ {c['code']}</span></div><div class="eyebrow">LEON / {c['code']}</div><h1>{E(c['title'])}</h1><p>{E(c['description'])}</p><p class="course-meta">{len(c['topics'])} {description}</p><div class="actions"><a class="button primary" href="{entry}">{entry_label} ↓</a><a class="button" href="../notes/{note_name(c,lang)}" download>{lab['notes']} ↓</a><a class="button" href="../cheatsheets/{slug}{suffix(lang)}">{lab['cheatweb']} ↗</a></div></header>{roadmap_html(c,lang)}{path_html(c,lang)}{course_reading_tools(c['code'],lang)}<div class="course-layout"><aside class="toc" aria-label="{lab['contents']}"><details open><summary>{lab['contents']}</summary>{extras}<a class="toc-group" href="#framework">{lab['map']}</a><ol>{toc}</ol><a class="toc-group" href="../cheatsheets/{slug}{suffix(lang)}">{lab['cheatweb']} ↗</a></details></aside><div class="course-body"><section class="overview"><h2>{lab['overview']}</h2><p class="scope">{E(c['coverage'])}</p><div class="overview-cols"><div><h3>{lab['before']}</h3><ul>{''.join('<li>'+E(x)+'</li>' for x in c['prerequisites'])}</ul></div><div><h3>{lab['outcomes']}</h3><ul>{''.join('<li>'+E(x)+'</li>' for x in c['outcomes'])}</ul></div></div></section><section class="framework" id="framework" data-reading-id="framework"><h2>{lab['map']}</h2><p>{lab['mapintro']}</p>{stages}</section>{''.join(lessons)}<section class="references" id="references" data-reading-id="references"><h2>{lab['references']}</h2><ul>{refs}</ul><p class="scope">{lab['scope']}</p></section></div></div>'''
    (SITE/'courses'/f'{slug}{suffix(lang)}').write_text(shell(c,lang,body))
    cheat=f'''<div class="cheat-page"><header class="course-hero"><div class="breadcrumb"><a href="../courses/{slug}{suffix(lang)}">← {c['code']}</a></div><div class="eyebrow">LEON / REFERENCE</div><h1>{E(c['title'])}</h1><p>{lab['reference']}</p><div class="actions"><a class="button primary" href="../downloads/{c['code']}-cheatsheet.pdf" download>{lab['cheat']} ↓</a><button class="button" data-print type="button">{lab['print']}</button></div></header>{roadmap_html(c,lang,'../courses/'+slug+suffix(lang))}<div class="cheat-grid">'''+''.join(f'<section class="cheat-item"><h2>{i+1:02d} / {E(x["title"])}</h2>{para(x["body"])}</section>' for i,x in enumerate(c['cheatsheet']))+'</div><span class="watermark">Leon</span></div>'
    (SITE/'cheatsheets'/f'{slug}{suffix(lang)}').write_text(shell(c,lang,cheat,True))
    md=[f'# {c["code"]} — {c["title"]}', '> Leon | Original study notes',f'[English]({c["code"]}.md) · [中文]({c["code"]}.zh.md)',roadmap_markdown(c,lang),c['description'],c['coverage'],path_md(c,lang),'## '+lab['map']]
    for stage in c['map']:md.append('### '+stage['title']+'\n'+ '\n'.join(f'- [{topics[k]["title"]}](#{k})' for k in stage['topics']))
    if c['code']=='COMP2123':md.append(run_notes(lang))
    for t in c['topics']:
        md.extend([f'<a id="{t["id"]}"></a>',f'## {t["title"]}',coach_md(c,t,lang),'### '+lab['story'],t['story'],'### '+lab['principle'],t['principle'],'### '+lab['formula'],'```text\n'+t['formula']+'\n```',t['symbols'],'### '+lab['example'],t['example']])
        if t.get('code'):
            md.append('```'+t.get('language','text')+'\n'+t['code']+'\n```')
            if illustration_notes(t,lang):
                instruction, commands = illustration_notes(t,lang).split('\n\n',1)
                md.extend([instruction,'```sh\n'+commands+'\n```'])
        md.extend([teaching_markdown(t,c['code'],lang),'**'+lab['pitfall']+':** '+t['pitfall'],'<details>\n<summary>'+lab['check']+'</summary>\n\n'+t['check']['question']+'\n\n'+t['check']['answer']+'\n\n</details>'])
    md+=['## '+lab['references']]+[f'- [{x["title"]}]({x["url"]})' for x in c.get('references',[])]+['\n---\nLeon']
    text='\n\n'.join(x for x in md if x)+'\n'
    (SITE/'notes'/note_name(c,lang)).write_text(text)
    (ROOT/'notes'/note_name(c,lang)).write_text(text.replace('](../assets/','](../site/assets/').replace('](../projects/','](../site/projects/'))


def course(c):
    edition(c,'en')
    translation=ROOT/'content'/'translations'/f'{c["code"]}.zh.json'
    if translation.exists():edition(json.loads(translation.read_text()),'zh')
