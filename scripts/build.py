#!/usr/bin/env python3
"""Build an offline-capable static portfolio and course library from reviewed JSON."""
from pathlib import Path
import html,json,re
from build_paths import build_all
from teaching import run_notes,asset_version,glossary_html,teaching_html,teaching_markdown,reading_tools,export_examples
ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'site'; CONTENT=ROOT/'content'
ORDER=['INFO1113','COMP2017','COMP2123','COMP2022','COMP3308']
E=lambda x:html.escape(str(x),quote=True)
def para(x):return ''.join('<p>'+E(p).replace('\n','<br>')+'</p>' for p in x.split('\n\n') if p)
def badge(x):return f'<span class="pill">{E(x)}</span>'
def shell(title,body,depth=0,description='Computer science, research and study notes by Leon Wang.',course=False):
 base='../'*depth
 gh=f'<a class="nav-github" href="{E(profile["github"])}">GitHub ↗</a>' if profile['github'] else ''
 return f'''<!doctype html>
<html lang="en" data-theme="dark"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{E(description)}"><meta name="theme-color" content="#090e17"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(description)}"><meta property="og:type" content="website"><title>{E(title)} | Leon</title><link rel="icon" href="{base}assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{base}assets/style.css?v={asset_version("style.css")}"><script defer src="{base}assets/app.js?v={asset_version("app.js")}"></script></head><body><a class="skip" href="#main">Skip to content</a><header class="topbar"><div class="wrap"><a class="brand" href="{base}index.html" translate="no"><span class="monogram">LW</span> Leon<span style="color:var(--accent)">.</span></a><nav aria-label="Main navigation"><a href="{base}index.html#projects">Projects</a><a href="{base}learn/">Learning</a><a class="nav-research" href="{base}index.html#research">Research</a><a href="{base}index.html#about">About</a>{gh}<button class="theme-button" type="button" data-theme-toggle aria-label="Switch to light theme">☼</button></nav></div></header><main id="main" class="wrap">{body}<footer class="footer"><div><span class="watermark">Leon</span><br>Research, ideas & learning in public.</div><div>Original explanations · Computer science & AI<br><a href="{base}learn/">Open the learning hub ↗</a></div><span>© 2026 Leon Wang</span></footer></main></body></html>'''
def orbital():
 return '''<div class="orbital" aria-label="Diagram connecting research, systems and learning"><svg viewBox="0 0 460 365" role="img" aria-labelledby="orbitTitle"><title id="orbitTitle">Ideas connect across research, systems and learning</title><defs><radialGradient id="glow"><stop stop-color="#b8ee91" stop-opacity=".09"/><stop offset="1" stop-color="#b8ee91" stop-opacity="0"/></radialGradient></defs><circle cx="236" cy="178" r="177" fill="url(#glow)"/><circle class="orbit" cx="236" cy="178" r="155"/><circle class="orbit" cx="236" cy="178" r="118" stroke-dasharray="3 8"/><ellipse class="orbit" cx="236" cy="178" rx="181" ry="78" transform="rotate(-35 236 178)"/><ellipse class="orbit" cx="236" cy="178" rx="181" ry="78" transform="rotate(35 236 178)"/><path class="path" d="M117 79L358 100L367 245L150 297L117 79M117 79L367 245M358 100L150 297"/><circle class="dot" cx="117" cy="79" r="4"/><circle class="dot" cx="358" cy="100" r="4"/><circle class="dot" cx="367" cy="245" r="4"/><circle class="dot" cx="150" cy="297" r="4"/><circle class="core" cx="236" cy="178" r="52"/><text class="core-label" x="236" y="178" text-anchor="middle">LW</text><text class="core-sub" x="236" y="197" text-anchor="middle">CONNECT IDEAS</text><text x="55" y="61">MULTIMODAL AI</text><text x="335" y="80">SYSTEMS</text><text x="341" y="268">REASONING</text><text x="70" y="320">LEARNING</text><text x="231" y="31" font-size="8">01 / EXPLORE</text></svg><span class="figure-caption">RESEARCH × FOUNDATIONS × EXPLANATION</span></div>'''
PROJECTS=[
 dict(id='loopdesk',name='LoopDesk',color='#4c9bff',tag='Agent',en='Evidence-first customer-service agent',zh='企业客服助手：能查订单、办退款，关键操作先等人工确认，每句回答都有依据',stack=['FastAPI + React','RAG','Human approval'],note='Static demo replaying an offline backend run · fictional data',demo='https://leon1111-wgl.github.io/loopdesk/'),
 dict(id='proofbi',name='ProofBI',color='#34d399',tag='ChatBI',en='Ask data in plain words; every number traces back',zh='用大白话问数据，自动查数出表，每个数字都能追到来源',stack=['Semantic layer','SQL guard','Row-level security'],note='Offline rules model on SYNTHETIC data · real-model evaluation pending',demo=''),
 dict(id='adproof',name='AdProof',color='#ff6b5b',tag='Multi-agent',en='Ad-copy compliance review with cited law text',zh='检查广告文案是否违规，标出问题句和对应法规，并给出改写建议',stack=['Multi-agent','Verified law snapshots','Rewrite re-review'],note='Offline numbers on SYNTHETIC scripts · law text from verified snapshots',demo=''),
 dict(id='creditlens',name='CreditLens',color='#a78bfa',tag='Multimodal',en='Financial figures checked back to the source page',zh='读财报表格取数，核对单位与口径，保留原文页码和定位证据',stack=['OCR','Table lookup','Comparability checks'],note='In development · saved results from public filings',demo=''),
 dict(id='estateguard',name='EstateGuard',color='#f5a524',tag='Vision',en='Community inspection with in-browser vision',zh='在浏览器里看小区巡检画面，找出违停、堆物等问题，再交给人工确认',stack=['D-FINE-N','DINOv2 parking','Human review'],note='Runs in your browser · real-site accuracy not yet validated',demo='https://leon1111-wgl.github.io/estateguard/'),
 dict(id='finscope',name='FinScope',color='#22c3d6',tag='Finance',en='Earnings quality from SEC filings',zh='读美股公司的财报（SEC 文件），看利润有没有水分',stack=['SEC filings','Anomaly triage','Stress scenarios'],note='Official annual filings with explicit source dates',demo='https://leon1111-wgl.github.io/finscope/'),
]
def project_card(p):
 code=f'https://github.com/leon1111-wgl/{p["id"]}'
 main=p['demo'] or code
 demo=f'<a class="button primary" href="{E(p["demo"])}">Demo <span>↗</span></a>' if p['demo'] else ''
 return f'''<article class="proj-card" style="--proj:{p['color']}"><div class="proj-top"><img src="assets/icons/{p['id']}.svg" width="30" height="30" alt=""><h3><a href="{E(main)}" translate="no">{E(p['name'])}</a></h3><span class="proj-tag">{E(p['tag'])}</span></div><p class="proj-en">{E(p['en'])}</p><p class="proj-zh" lang="zh-CN">{E(p['zh'])}</p><ul class="proj-stack">{''.join(f'<li>{E(s)}</li>' for s in p['stack'])}</ul><p class="proj-note">{E(p['note'])}</p><div class="proj-actions">{demo}<a class="button" href="{code}">Code <span>↗</span></a></div></article>'''
def hub_panel():
 from build_learn import catalogue
 from build_learn_card import map_svg
 d=catalogue();t=d['totals'];byid={c['id']:c for c in d['courses']}
 route=''.join(f'<li data-track="{r['track']}"><span class="hub-track">{E(d["tracks"][r["track"]]["en"])}</span><span class="hub-chips">'+''.join(f'<a href="learn/#/course/{cid}" style="--c:{E(byid[cid]["color"])}">{E(byid[cid]["short"]["en"])}</a>' for cid in r['courses'])+'</span></li>' for r in d['route'])
 return f'''<section id="learning" class="section"><div class="section-head"><div><span class="number">02 / LEARNING HUB · <span lang="zh-CN">学习中心</span></span><h2>Learn to code from zero, in English and Chinese.</h2></div><p>Python, Java, C, algorithms, computation and AI, in one suggested order. Pick a house on the map to open its course.</p></div><div class="hub-panel"><div class="hub-copy"><p class="hub-zh" lang="zh-CN">从零学会编程，中英双语</p><dl class="hub-stats"><div><dt>Courses</dt><dd>{t['courses']}</dd></div><div><dt>Chapters</dt><dd>{t['chapters']}</dd></div><div><dt>Runnable programs</dt><dd>{t['programs']}</dd></div><div><dt>One-page sheets</dt><dd>{t['sheets']}</dd></div></dl><ol class="hub-route">{route}</ol><div class="actions"><a class="button primary" href="learn/">Open the learning hub <span>↗</span></a><a class="button" href="python-zero-to-practice/index.html">Start with Python <span>↗</span></a><a class="text-link" href="downloads/guoliang-cheatsheet-collection.pdf" download>All cheatsheets (PDF) ↓</a></div></div><div class="hub-map-wrap">{map_svg()}</div></div></section>'''
def home(courses,guides):
 r=profile['research']
 ed=''.join(f'<li><time>{E(x["period"])}</time><h3>{E(x["institution"])}</h3><p>{E(x["degree"])}<br>{E(x["detail"])}</p></li>' for x in profile['education'])
 exp=''.join(f'<li><time>{E(x["period"])}</time><h3>{E(x["role"])}</h3><p>{E(x["organization"])}<br>{E(x["detail"])}</p></li>' for x in profile['experience'])
 projects=f'''<section id="projects" class="section"><div class="section-head"><div><span class="number">01 / PROJECTS</span><h2>From model outputs to useful decisions.</h2></div><p>Six projects, {['no','one','two','three','four','five','all six'][sum(1 for p in PROJECTS if p['demo'])]} with live demos so far. Each card says what is not yet proven.</p></div><div class="proj-grid">{''.join(project_card(p) for p in PROJECTS)}</div></section>'''
 body=f'''<div class="hero"><div><div class="eyebrow"><span class="live-dot"></span> LEON WANG / AI APPLICATIONS & RESEARCH</div><h1>Exploring intelligence.<br><span>Sharing understanding.</span></h1><p class="intro">{E(profile['bio'])}</p><div class="actions"><a class="button primary" href="#projects">Explore projects <span>↓</span></a><a class="button" href="learn/">Open the learning hub <span>↗</span></a></div><p class="hero-note">HONG KONG · SYDNEY &nbsp; / &nbsp; CURIOSITY, MADE PRACTICAL</p></div>{orbital()}</div><div class="meta-strip"><div class="meta-item"><div class="meta-symbol">⌘</div><div><strong>MSc student</strong><span>The University of Hong Kong · 2026 - Present</span></div></div><div class="meta-item"><div class="meta-symbol">✳</div><div><strong>Evidence-grounded video understanding</strong><span>AAAI 2025</span></div></div><div class="meta-item"><div class="meta-symbol">06</div><div><strong>Applied AI projects</strong><span>Agents · ChatBI · compliance · vision · finance</span></div></div></div>
{projects}{hub_panel()}
<section id="research" class="section"><div class="section-head"><div><span class="number">03 / SELECTED RESEARCH</span><h2>Answers should come with evidence.</h2></div></div><article class="research-panel"><div>{badge(r['venue'])}<h3>{E(r['title'])}</h3><p>{E(r['summary'])}</p><a class="text-link" href="{E(r['url'])}">Read the publication ↗</a></div><div class="research-side"><h4>My contribution</h4><p>{E(r['contribution'])}</p><p><span class="pill">Long video</span><span class="pill">Evaluation</span></p></div></article></section>
<section id="about" class="section"><div class="section-head"><div><span class="number">04 / A LITTLE CONTEXT</span><h2>A background built across disciplines.</h2></div><p>I use stories, small examples, and careful definitions to make technical ideas easier to revisit.</p></div><div class="about-grid"><div><p class="eyebrow">EDUCATION</p><ul class="timeline">{ed}</ul><div class="skills">{''.join(f'<span>{E(s)}</span>' for s in profile['skills'])}</div><p>{E(profile['languages'])}</p></div><div><p class="eyebrow">EXPERIENCE</p><ul class="timeline">{exp}</ul><a class="text-link" href="mailto:{E(profile['email'])}">Get in touch ↗</a></div></div></section>'''
 (SITE/'index.html').write_text(shell('Leon Wang — AI Applications, Research & Learning',body,description='Applied AI projects, research and a bilingual learning hub by Leon Wang.'))
from build_courses import course
def readme(courses,guides):
 from build_profile import build_profile
 build_profile(ROOT,profile,courses,guides)
if __name__=='__main__':
 profile=json.loads((CONTENT/'profile.json').read_text())
 courses=[json.loads((CONTENT/(c+'.json')).read_text()) for c in ORDER]
 for name in ['courses','cheatsheets','downloads','notes','assets']:(SITE/name).mkdir(parents=True,exist_ok=True)
 (ROOT/'notes').mkdir(exist_ok=True)
 (ROOT/'profile').mkdir(exist_ok=True)
 for c in courses:course(c)
 guides=build_all(ROOT,profile)
 primer_path=CONTENT/'primer.json'
 primer=json.loads(primer_path.read_text()) if primer_path.exists() else None
 if primer:
  from build_paths import build_one
  build_one(ROOT,profile,primer)
 export_examples([(c['code'],c) for c in courses]+[('AI-'+g['code'],g) for g in guides]+([('AI-START',primer)] if primer else []))
 from build_projects import build_all as build_projects
 build_projects()
 from build_python_course import build as build_python_course
 build_python_course()
 home(courses,guides);readme(courses,guides)
 (SITE/'.nojekyll').write_text('')
 print(f'Built {len(courses)} bilingual courses ({sum(len(c["topics"]) for c in courses)} topics) and {len(guides)} bilingual AI guides ({sum(len(g["topics"]) for g in guides)} topics), HTML and Markdown.')
