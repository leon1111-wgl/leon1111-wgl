#!/usr/bin/env python3
"""Build an offline-capable static portfolio and course library from reviewed JSON."""
from pathlib import Path
import html,json,re
from build_paths import build_all,home_section
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
<html lang="en" data-theme="dark"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{E(description)}"><meta name="theme-color" content="#090e17"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(description)}"><meta property="og:type" content="website"><title>{E(title)} | Leon</title><link rel="icon" href="{base}assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{base}assets/style.css?v={asset_version("style.css")}"><script defer src="{base}assets/app.js?v={asset_version("app.js")}"></script></head><body><a class="skip" href="#main">Skip to content</a><header class="topbar"><div class="wrap"><a class="brand" href="{base}index.html"><span class="monogram">LW</span> Leon<span style="color:var(--accent)">.</span></a><nav aria-label="Main navigation"><a href="{base}index.html#learning">Learning</a><a class="nav-ai" href="{base}index.html#ai">AI</a><a class="nav-research" href="{base}index.html#research">Research</a><a href="{base}index.html#about">About</a>{gh}<button class="theme-button" type="button" data-theme-toggle aria-label="Switch to light theme">☼</button></nav></div></header><main id="main" class="wrap">{body}<footer class="footer"><div><span class="watermark">Leon</span><br>Research, ideas & learning in public.</div><div>Original explanations · Computer science & AI<br><a href="{base}index.html#learning">Explore the learning library ↑</a></div><span>© 2026 Leon Wang</span></footer></main></body></html>'''
def orbital():
 return '''<div class="orbital" aria-label="Diagram connecting research, systems and learning"><svg viewBox="0 0 460 365" role="img" aria-labelledby="orbitTitle"><title id="orbitTitle">Ideas connect across research, systems and learning</title><defs><radialGradient id="glow"><stop stop-color="#b8ee91" stop-opacity=".09"/><stop offset="1" stop-color="#b8ee91" stop-opacity="0"/></radialGradient></defs><circle cx="236" cy="178" r="177" fill="url(#glow)"/><circle class="orbit" cx="236" cy="178" r="155"/><circle class="orbit" cx="236" cy="178" r="118" stroke-dasharray="3 8"/><ellipse class="orbit" cx="236" cy="178" rx="181" ry="78" transform="rotate(-35 236 178)"/><ellipse class="orbit" cx="236" cy="178" rx="181" ry="78" transform="rotate(35 236 178)"/><path class="path" d="M117 79L358 100L367 245L150 297L117 79M117 79L367 245M358 100L150 297"/><circle class="dot" cx="117" cy="79" r="4"/><circle class="dot" cx="358" cy="100" r="4"/><circle class="dot" cx="367" cy="245" r="4"/><circle class="dot" cx="150" cy="297" r="4"/><circle class="core" cx="236" cy="178" r="52"/><text class="core-label" x="236" y="178" text-anchor="middle">LW</text><text class="core-sub" x="236" y="197" text-anchor="middle">CONNECT IDEAS</text><text x="55" y="61">MULTIMODAL AI</text><text x="335" y="80">SYSTEMS</text><text x="341" y="268">REASONING</text><text x="70" y="320">LEARNING</text><text x="231" y="31" font-size="8">01 / EXPLORE</text></svg><span class="figure-caption">RESEARCH × FOUNDATIONS × EXPLANATION</span></div>'''
def home(courses,guides):
 python_portal='''<article class="research-panel" id="python" style="margin-bottom:32px"><div><span class="eyebrow">LEON / PYTHON / START HERE</span><h3>Python — Zero to Practice</h3><p>Start with your first line of Python. Work through small examples, practise on your own, and build four complete projects. This handbook is in Chinese.</p><div class="actions"><a class="button primary" href="python-zero-to-practice/index.html">Read the Python handbook ↗</a><a class="button" href="downloads/Python-Zero-to-Practice.zip" download>Download the learning kit ↓</a></div></div><div class="research-side"><h4>Build a practical foundation</h4><p>19 learning units · 91 runnable examples<br>100 self-study exercises · 4 projects</p><p>Search chapters, follow visual demonstrations, and save your progress in your browser.</p><span class="pill">Python 3.10+</span><span class="pill">Standard library</span><span class="pill">Offline reading</span></div></article>'''
 cards=''.join(f'''<a class="course-card" href="courses/{c['code'].lower()}.html" data-course-base="courses/{c['code'].lower()}" style="--card-color:{E(c['color'])}"><div class="card-top"><span class="course-code">{E(c['code'])}</span><span>0{i+1} / NOTES</span></div><h3>{E(c['title'])}</h3><p>{E(c['subtitle'])}</p><div class="card-foot"><span>{len(c['topics']):02d} TOPICS · EN / ZH · MAP</span><span class="arrow" aria-hidden="true">↗</span></div></a>''' for i,c in enumerate(courses))
 cards += '<a class="course-card" href="downloads/guoliang-cheatsheet-collection.pdf" style="--card-color:var(--accent)"><div class="card-top"><span class="course-code">THE REFERENCE DESK</span><span>PDF / 05 PAGES</span></div><h3>Five courses.<br>One page each.</h3><p>Bring the core formulas, models, and decision rules together in one printable collection.</p><div class="card-foot"><span>LEON / CHEATSHEET COLLECTION</span><span class="arrow">↓</span></div></a>'
 ed=''.join(f'<li><time>{E(x["period"])}</time><h3>{E(x["institution"])}</h3><p>{E(x["degree"])}<br>{E(x["detail"])}</p></li>' for x in profile['education'])
 exp=''.join(f'<li><time>{E(x["period"])}</time><h3>{E(x["role"])}</h3><p>{E(x["organization"])}<br>{E(x["detail"])}</p></li>' for x in profile['experience'])
 r=profile['research'];count=sum(len(c['topics']) for c in courses)
 body=f'''<div class="hero"><div><div class="eyebrow"><span class="live-dot"></span> LEON WANG / RESEARCH & NOTES</div><h1>Exploring intelligence.<br><span>Sharing understanding.</span></h1><p class="intro">{E(profile['bio'])}</p><div class="actions"><a class="button primary" href="#learning">Explore the courses <span>↗</span></a><a class="button" href="#research">View research <span>↓</span></a></div><p class="hero-note">HONG KONG · SYDNEY &nbsp; / &nbsp; CURIOSITY, MADE PRACTICAL</p></div>{orbital()}</div><div class="meta-strip"><div class="meta-item"><div class="meta-symbol">⌘</div><div><strong>MSc student</strong><span>The University of Hong Kong · 2026 - Present</span></div></div><div class="meta-item"><div class="meta-symbol">✳</div><div><strong>Evidence-grounded video understanding</strong><span>Co-first author · AAAI 2026</span></div></div><div class="meta-item"><div class="meta-symbol">05</div><div><strong>Computer science learning paths</strong><span>{count} explanations · Five one-page references</span></div></div></div>
<section id="learning" class="section"><div class="section-head"><div><span class="number">01 / THE LEARNING LIBRARY</span><h2>Start with a story. Leave with a model.</h2></div><p>Explore a course, follow its knowledge map, and connect intuition to the mathematics.</p></div><div class="course-grid">{cards}</div><div class="method"><div><b>01 / IMAGINE</b><h3>An analogy story</h3><p>A familiar situation gives an abstract idea somewhere to begin.</p></div><div><b>02 / UNDERSTAND</b><h3>The underlying principle</h3><p>Explain the mechanism, its assumptions, and where the analogy stops.</p></div><div><b>03 / FORMALIZE</b><h3>The formula, unpacked</h3><p>Read each symbol and connect the equation to its meaning.</p></div><div><b>04 / APPLY</b><h3>A worked example</h3><p>Trace concrete steps, then test your understanding with a fresh question.</p></div></div><div class="actions"><a class="text-link" href="downloads/guoliang-cheatsheet-collection.pdf" download>Download all five one-page cheatsheets ↓</a></div></section>
{home_section(guides)}
<section id="research" class="section"><div class="section-head"><div><span class="number">03 / SELECTED RESEARCH</span><h2>Answers should come with evidence.</h2></div></div><article class="research-panel"><div>{badge(r['venue'])}{badge(r['role'])}<h3>{E(r['title'])}</h3><p>{E(r['summary'])}</p><a class="text-link" href="{E(r['url'])}">Read the publication ↗</a></div><div class="research-side"><h4>My contribution</h4><p>{E(r['contribution'])}</p><p><span class="pill">Long video</span><span class="pill">Evaluation</span></p></div></article></section>
<section id="about" class="section"><div class="section-head"><div><span class="number">04 / A LITTLE CONTEXT</span><h2>A background built across disciplines.</h2></div><p>I use stories, small examples, and careful definitions to make technical ideas easier to revisit.</p></div><div class="about-grid"><div><p class="eyebrow">EDUCATION</p><ul class="timeline">{ed}</ul><div class="skills">{''.join(f'<span>{E(s)}</span>' for s in profile['skills'])}</div><p>{E(profile['languages'])}</p></div><div><p class="eyebrow">EXPERIENCE</p><ul class="timeline">{exp}</ul><a class="text-link" href="mailto:{E(profile['email'])}">Get in touch ↗</a></div></div></section>'''
 body=body.replace('<div class="course-grid">',python_portal+'<div class="course-grid">',1)
 (SITE/'index.html').write_text(shell('Leon Wang — Research & Learning',body))
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
