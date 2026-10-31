#!/usr/bin/env python3
"""Render original bilingual AI field guides as static, directly linkable pages."""
from pathlib import Path
from roadmaps import roadmap_html, roadmap_markdown
from learning_extensions import extension_html, extension_markdown, extension_link
import html,json
from palette import COURSE_COLORS
from teaching import run_notes,asset_version,glossary_html,teaching_html,teaching_markdown,reading_tools,LEVELS
E=lambda x:html.escape(str(x),quote=True)
ORDER=['ml','dl','vision','multimodal']
LABELS={
'en':dict(hub='Leon Learn',detail='Course page',allcourses='All courses',startread='Start reading',nextch='Next: ',cases='Guided cases',tocshort='Contents',bilingual='Chinese + English',chapterof='Chapter {i} of {n}',notefoot='Independent study notes, not official course material.',home='Home',learning='Learning',contents='IN THIS GUIDE',map='Knowledge framework',route='A route through the ideas',before='Before you start',outcomes='What you will learn',jump='Choose a concept. Follow the story into the mathematics.',story='01 / The story',concept='02 / The concept',application='03 / Put the concept to work',practice='04 / How others use it',formula='05 / The formula, unpacked',calculation='06 / Work through the numbers',limits='Where the analogy stops',takeaway='Keep this idea',sources='Sources for this topic',references='Official tutorials & original research',review='The reference desk',back='Back to the framework',notes='Download these notes',print='Print this guide',note='Original stories, explanations and examples by Leon. The linked tutorials and research belong to their respective authors; these independent companions are not official translations or endorsed courses.',topics='chapters · stories, concepts, applications and formulas',footer='Research, ideas & learning in public.',switch='Reading language',all='Explore all four AI field guides'),
'zh':dict(hub='Leon 学习',detail='课程详情',allcourses='全部课程',startread='开始阅读',nextch='下一章：',cases='完整案例',tocshort='目录',bilingual='中英双语',chapterof='第 {i} 章 · 共 {n} 章',notefoot='独立整理的学习笔记，不是官方课程材料。',home='首页',learning='学习资料',contents='本学习路径',map='知识框架',route='把知识连接起来',before='开始前需要了解',outcomes='你将学到什么',jump='点击一个概念，从故事走向原理与数学。',story='01 / 从一个完整故事开始',concept='02 / 理解核心概念',application='03 / 如何运用这个概念',practice='04 / 官方教程与研究中的应用',formula='05 / 公式与逐项解析',calculation='06 / 一步步算出结果',limits='类比的边界与注意事项',takeaway='记住这一点',sources='本节资料来源',references='官方教程与原始研究',review='知识速查',back='返回知识框架',notes='下载当前语言讲义',print='打印这份讲义',note='故事、讲解与计算例子由 Leon 原创编写。链接中的教程和研究属于各自作者；本资料为独立学习笔记，并非官方译本或官方认可课程。',topics='个章节 · 故事、概念、应用和公式',footer='分享研究、想法与学习。',switch='阅读语言',all='浏览全部四条 AI 学习路径')}
def para(text):return ''.join('<p>'+E(p).replace('\n','<br>')+'</p>' for p in text.split('\n\n') if p)
def localized(item,lang):return item[lang]
def switcher(g,lang):
 links=''.join(f'<a href="{g["id"]}.{l}.html" lang="{l}" hreflang="{l}" data-language="{l}"'+(' aria-current="page"' if l==lang else '')+f'>{name}</a>' for l,name in [('en','EN'),('zh','中文')])
 return f'<div class="language-switch" role="navigation" aria-label="{LABELS[lang]["switch"]}">{links}</div>'
def shell(g,lang,body,profile):
 lab=LABELS[lang]; title=g['title'][lang]; switch=switcher(g,lang); iso='en' if lang=='en' else 'zh-Hans'
 return f'''<!doctype html><html lang="{iso}" data-theme="dark"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{E(g['description'][lang])}"><meta name="theme-color" content="#000000"><title>{E(title)} | Leon</title><link rel="alternate" hreflang="en" href="{g['id']}.en.html"><link rel="alternate" hreflang="zh-Hans" href="{g['id']}.zh.html"><link rel="icon" href="../assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="../assets/style.css?v={asset_version("style.css")}"><link rel="stylesheet" href="../assets/reader.css?v={asset_version("reader.css")}"><script defer src="../assets/app.js?v={asset_version("app.js")}"></script></head><body class="field-guide reader" data-course-id="{g['id']}" style="--course:{COURSE_COLORS[g['id']]}"><a class="skip" href="#main">{lab['map']}</a><header class="topbar reader-bar"><div class="wrap"><a class="brand" href="../learn/"><span class="monogram">LW</span>{lab['hub']}</a><a class="reader-back" href="../learn/#/course/{g['id']}">← {g['code']} · {lab['detail']}</a><nav aria-label="{lab['contents']}">{switch}<button class="theme-button" type="button" data-theme-toggle aria-label="Switch to light theme">☼</button></nav></div></header><main id="main" class="wrap">{body}<footer class="footer reader-foot"><span>{lab['notefoot']}</span><a href="../learn/#/courses">{lab['allcourses']} ↗</a><span>© 2026 Leon Wang</span></footer></main></body></html>'''
def topic_nav(g,i,lang,cases=False):
 """The end of a chapter: back to the contents, or straight on to the next chapter."""
 lab=LABELS[lang]; nxt=g['topics'][i+1] if i+1<len(g['topics']) else None
 end=('#extensions',lab['cases']) if cases else ('#review',lab['review'])
 link=f'<a class="next" href="#{nxt["id"]}">{lab["nextch"]}{E(nxt["title"][lang])} →</a>' if nxt else f'<a class="next" href="{end[0]}">{end[1]} →</a>'
 return f'<nav class="topic-nav"><a href="#framework">↑ {lab["tocshort"]}</a>{link}</nav>'
def page(g,lang,profile):
 lab=LABELS[lang]; ids={t['id']:t for t in g['topics']}; refs={r['id']:r for r in g['references']}
 toc=''.join(f'<li><a href="#{t["id"]}">{E(t["title"][lang])}</a></li>' for t in g['topics'])
 stages=''.join(f'<div class="map-stage"><h3>{i+1:02d} / {E(s["title"][lang])}</h3><div class="map-nodes">'+''.join(f'<a href="#{k}">{E(ids[k]["title"][lang])}</a>' for k in s['topics'])+'</div></div>' for i,s in enumerate(g['map']))
 sections=[];cases=extension_html(g,lang)
 for i,t in enumerate(g['topics']):
  sources=''.join(f'<li><a href="{E(refs[k]["url"])}">{E(refs[k]["publisher"])} · {E(refs[k]["title"][lang])} ↗</a></li>' for k in t['sources'])
  sections.append(f'''<article class="topic guide-topic" id="{t['id']}" data-reading-id="{t['id']}"><div class="topic-head"><span class="topic-number">{lab['chapterof'].format(i=i+1,n=len(g['topics']))}</span></div><h2>{E(t['title'][lang])}</h2>{('<span class="level-label">'+LEVELS[t['level']][lang]+'</span>') if t.get('level') else ''}<div class="story guide-story"><h3>{lab['story']}</h3>{para(t['story'][lang])}</div><div class="guide-concept"><h3>{lab['concept']}</h3>{para(t['concept'][lang])}</div>{glossary_html(t,lang)}<div class="guide-application-grid"><div><h3>{lab['application']}</h3>{para(t['application'][lang])}</div><div class="guide-practice"><h3>{lab['practice']}</h3>{para(t['practice'][lang])}</div></div><div class="formula"><h3>{lab['formula']}</h3><pre>{E(t['formula'])}</pre>{para(t['symbols'][lang])}</div><div class="example"><h3>{lab['calculation']}</h3>{para(t['calculation'][lang])}</div>{teaching_html(t,'AI-'+g['code'],lang)}<div class="pitfall"><strong>{lab['limits']}.</strong> {E(t['limits'][lang])}</div><div class="takeaway"><span>{lab['takeaway']}</span>{para(t['takeaway'][lang])}</div><div class="topic-sources"><h3>{lab['sources']}</h3><ul>{sources}</ul></div>{topic_nav(g,i,lang,bool(cases))}</article>''')
 review=''.join(f'<a class="cheat-item" href="#{g["topics"][i]["id"]}"><h3>{i+1:02d} / {E(r["title"][lang])}</h3><p>{E(r["body"][lang])}</p></a>' for i,r in enumerate(g['review']))
 references=''.join(f'<li id="ref-{r["id"]}"><a href="{E(r["url"])}">{E(r["title"][lang])} ↗</a><span>{E(r["publisher"])} · {E(r["kind"])}</span></li>' for r in g['references'])
 content=f'''<header class="course-hero" id="top"><div class="reader-tags"><span class="code-chip">{g['code']}</span><span class="tag">{lab['bilingual']}</span></div><h1>{E(g['title'][lang])}</h1><p>{E(g['description'][lang])}</p><div class="actions"><a class="button primary" href="#{g['topics'][0]['id']}">{lab['startread']} ↓</a><a class="button" href="#references">{lab['references']} ↗</a><a class="button" href="../notes/AI-{g['code']}.{lang}.md" download>{lab['notes']} ↓</a></div><p class="course-meta">{len(g['topics'])} {lab['topics']}</p></header>{reading_tools(lang,g["id"]!="start")}<div class="course-layout"><aside class="toc" aria-label="{lab['contents']}"><details open><summary>{lab['contents']}</summary>{extension_link(g,lang)}<a class="toc-group" href="#framework">{lab['map']}</a><ol>{toc}</ol><a class="toc-group" href="#review">{lab['review']}</a><a class="toc-group" href="#references">{lab['references']}</a></details></aside><div class="course-body"><section class="overview"><h2>{lab['route']}</h2><p class="scope">{E(g['coverage'][lang])}</p><div class="overview-cols"><div><h3>{lab['before']}</h3><ul>{''.join('<li>'+E(x)+'</li>' for x in g['prerequisites'][lang])}</ul></div><div><h3>{lab['outcomes']}</h3><ul>{''.join('<li>'+E(x)+'</li>' for x in g['outcomes'][lang])}</ul></div></div></section><section class="framework" id="framework" data-reading-id="framework"><h2>{lab['map']}</h2><p>{lab['jump']}</p>{stages}</section>{''.join(sections)}{cases}<section id="review" class="guide-review" data-reading-id="review"><h2>{lab['review']}</h2><div class="guide-review-grid">{review}</div></section><section class="references" id="references" data-reading-id="references"><h2>{lab['references']}</h2><p class="source-note">{lab['note']}</p><ol class="source-list">{references}</ol></section></div></div>'''
 return shell(g,lang,content,profile)
def markdown(g,lang):
 lab=LABELS[lang]; refs={r['id']:r for r in g['references']}; topics={t['id']:t for t in g['topics']}
 chunks=[f'# {g["title"][lang]}', '> Leon | AI Field Guides', f'[EN](AI-{g["code"]}.en.md) · [中文](AI-{g["code"]}.zh.md)',roadmap_markdown(g,lang),extension_markdown(g,lang),g['description'][lang],run_notes(lang),f'## {lab["route"]}',g['coverage'][lang],f'### {lab["before"]}']
 chunks.append('\n'.join('- '+x for x in g['prerequisites'][lang]))
 chunks.extend([f'### {lab["outcomes"]}','\n'.join('- '+x for x in g['outcomes'][lang]),f'## {lab["map"]}'])
 for stage in g['map']:
  chunks.append(f'### {stage["title"][lang]}')
  chunks.append('\n'.join(f'- [{topics[k]["title"][lang]}](#{k})' for k in stage['topics']))
 for t in g['topics']:
  chunks.extend([f'<a id="{t["id"]}"></a>',f'## {t["title"][lang]}'])
  for key in ['story','concept','application','practice']:chunks.extend([f'### {lab[key]}',t[key][lang]])
  chunks.extend([f'### {lab["formula"]}','```text\n'+t['formula']+'\n```',t['symbols'][lang],f'### {lab["calculation"]}',t['calculation'][lang]])
  if t.get('code_examples'):chunks.append(teaching_markdown(t,'AI-'+g['code'],lang))
  chunks.extend([f'**{lab["limits"]}:** '+t['limits'][lang],f'**{lab["takeaway"]}:** '+t['takeaway'][lang],f'### {lab["sources"]}'])
  for k in t['sources']:chunks.append(f'- [{refs[k]["publisher"]}: {refs[k]["title"][lang]}]({refs[k]["url"]})')
 chunks.append(f'## {lab["review"]}')
 for i,r in enumerate(g['review']):chunks.extend([f'### [{r["title"][lang]}](#{g["topics"][i]["id"]})',r['body'][lang]])
 chunks.extend([f'## {lab["references"]}',lab['note']])
 for r in g['references']:chunks.append(f'- [{r["title"][lang]}]({r["url"]}) — {r["publisher"]}')
 return '\n\n'.join(chunks)+'\n'
def home_section(guides):
 if not guides:return ''
 cards=''.join(f'''<article class="ai-card" style="--guide-color:{E(g['color'])}"><a class="ai-card-main" href="ai/{g['id']}.en.html" data-guide-base="ai/{g['id']}"><div class="card-top"><span class="course-code">{g['code']}</span><span>{len(g['topics']):02d} / FIELD GUIDE</span></div><h3>{E(g['title']['en'])}</h3><p>{E(g['subtitle']['en'])}</p><span class="text-link">Follow the story ↗</span></a><div class="ai-card-foot"><span>Leon · Original explanations</span><a href="ai/{g['id']}.en.html" lang="en">EN</a><a href="ai/{g['id']}.zh.html" lang="zh">ZH</a></div></article>''' for g in guides)
 return f'''<section class="section ai-section" id="ai"><div class="section-head"><div><span class="number">02 / AI FIELD GUIDES · EN + ZH</span><h2>Four ways into artificial intelligence.</h2></div><p>Learn one idea at a time. Start with a story. Follow the maths. Run Python and check its output. Each guide moves from the basics to common applications.</p></div><div class="primer-callout"><div><h3>New to Python or AI?</h3><p>Begin with eight short lessons on Python, vectors, probability and gradients. No prior AI knowledge is needed.</p></div><div class="actions"><a class="button primary" href="ai/start.en.html">Start here · EN ↗</a><a class="button" href="ai/start.zh.html" lang="zh" aria-label="Read the beginner primer in Chinese">Start here · ZH ↗</a></div></div><div class="ai-grid">{cards}</div><p class="source-note">Independent bilingual companions to official tutorials and original research from Google, PyTorch, scikit-learn, Stanford, OpenCV, Hugging Face and the research community. Every topic links to its sources.</p></section>'''
def readme_section(guides,site_url):
 if not guides:return ''
 text='## AI field guides · English / Chinese\n\nOriginal stories, concepts, real applications and worked mathematics, with references to official tutorials and original research. Each guide moves from the basics to practical applications, with runnable Python and a language switch.\n\n| Field guide | English | Chinese |\n| :--- | :--- | :--- |\n'
 for g in guides:
  base=site_url+'ai/'+g['id'] if site_url else 'site/ai/'+g['id']
  text+=f'| {g["title"]["en"]} | [Read]({base}.en.html) | [Read]({base}.zh.html) |\n'
 return text+'\n'
def build_one(root,profile,g):
 for lang in ['en','zh']:
  (root/'site'/'ai'/f'{g["id"]}.{lang}.html').write_text(page(g,lang,profile))
  note=markdown(g,lang)
  for destination in [root/'site'/'notes',root/'notes']:
   (destination/f'AI-{g["code"]}.{lang}.md').write_text(note.replace('](../assets/','](../site/assets/') if destination==root/'notes' else note)
def build_all(root,profile):
 guides=[];site=root/'site'
 for folder in [site/'ai',site/'notes',root/'notes']:folder.mkdir(parents=True,exist_ok=True)
 for name in ORDER:
  source=root/'content'/'paths'/(name+'.json')
  if not source.exists():continue
  g=json.loads(source.read_text());guides.append(g)
  build_one(root,profile,g)
 return guides
