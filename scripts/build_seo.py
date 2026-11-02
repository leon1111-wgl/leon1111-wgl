#!/usr/bin/env python3
"""Write the files that help people find the site: sitemap.xml, robots.txt and the share images.

    python scripts/build_seo.py           sitemap.xml and robots.txt only
    python scripts/build_seo.py --images  also redraw the PNG share cards (needs Google Chrome)

Share cards (site/assets/og/):
- home.png and learn.png (1200 x 630) are the Open Graph images of the homepage and the learning pages;
- repo-<name>.png (1280 x 640) are GitHub social previews. GitHub has no API for these: upload each one by hand
  under the repository's Settings > General > Social preview.
Every word on a card comes from the homepage project list or the course catalogue, so the cards make no new claims.
"""
from html import escape as E
from pathlib import Path
import json
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_learn import MAP, catalogue
from build_learn_card import smooth
import seo

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'
OG = SITE / 'assets' / 'og'
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'


# ------------------------------------------------------------------ sitemap and robots
def pages():
    """(path, alternates) for every page worth finding; alternates pairs the English and Chinese editions."""
    data = catalogue()
    yield '', None
    yield 'learn/', None
    for c in data['courses']:
        read = c['read']
        if len(read) == 1:
            yield next(iter(read.values())), None
            continue
        for kind in ('read', 'sheet'):
            alts = {l: c[kind][l] for l in ('en', 'zh')}
            if any('#' in p for p in alts.values()):
                continue  # a guide's review is a section of its reading page, not a page of its own
            for l in ('en', 'zh'):
                yield alts[l], alts
    projects = sorted(p.name for p in (SITE / 'projects').glob('*.en.html'))
    for name in projects:
        base = name.removesuffix('.en.html')
        alts = {'en': f'projects/{base}.en.html', 'zh': f'projects/{base}.zh.html'}
        for l in ('en', 'zh'):
            yield alts[l], alts
    for pdf in sorted((SITE / 'downloads').glob('*cheatsheet*.pdf')):
        yield f'downloads/{pdf.name}', None


def sitemap():
    rows = []
    for path, alts in pages():
        assert (SITE / (path or 'index.html')).is_file() or (SITE / path / 'index.html').is_file(), path
        links = ''.join(f'<xhtml:link rel="alternate" hreflang="{seo.ISO[l]}" href="{seo.url(p)}"/>' for l, p in alts.items()) if alts else ''
        if alts:
            links += f'<xhtml:link rel="alternate" hreflang="x-default" href="{seo.url(alts["en"])}"/>'
        rows.append(f'  <url><loc>{seo.url(path)}</loc>{links}</url>')
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
           + '\n'.join(rows) + '\n</urlset>\n')
    (SITE / 'sitemap.xml').write_text(xml)
    (SITE / 'robots.txt').write_text(
        '# This site is a GitHub Pages project site under /leon1111-wgl/. Crawlers only read robots.txt at the\n'
        '# root of a host, so this copy just names the sitemap for tools that look here.\n'
        f'User-agent: *\nAllow: /\n\nSitemap: {seo.url("sitemap.xml")}\n')
    return len(rows)


# ------------------------------------------------------------------ share cards
BASE_CSS = '''*{box-sizing:border-box;margin:0}html,body{width:W;height:H;overflow:hidden}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Hiragino Sans GB",sans-serif;-webkit-font-smoothing:antialiased}
.mono{font-family:ui-monospace,"SF Mono",Menlo,monospace}'''


def page(w, h, css, body):
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{BASE_CSS.replace("W", f"{w}px").replace("H", f"{h}px")}{css}</style>'
            f'</head><body>{body}</body></html>')


def project_list():
    from build import PROJECTS
    return PROJECTS


def home_card(w, h):
    chips = ''.join(f'<span style="--c:{p["color"]}"><i></i>{E(p["name"])}</span>' for p in project_list())
    css = '''body{background:#090e17;color:#eaf0f6;position:relative;padding:64px 72px}
.glow{position:absolute;inset:0;background:radial-gradient(ellipse 40% 55% at 82% 40%,rgb(184 238 145/.10),transparent 70%),radial-gradient(ellipse 30% 40% at 95% 90%,rgb(183 167 239/.12),transparent 70%)}
svg.orbit{position:absolute;right:-30px;top:80px;width:470px;height:470px;opacity:.9}
.eyebrow{display:flex;align-items:center;gap:14px;font-size:17px;letter-spacing:2.5px;color:#b8ee91}
.eyebrow b{display:grid;place-items:center;width:44px;height:44px;border-radius:12px;background:#b8ee91;color:#090e17;font:700 17px/1 ui-monospace,Menlo,monospace;letter-spacing:0}
h1{position:relative;margin-top:44px;font-size:70px;line-height:1.08;font-weight:800;letter-spacing:-1.5px}
h1 span{color:#9faebe}
p.sub{position:relative;margin-top:26px;font-size:24px;line-height:1.5;color:#c6d1dd;max-width:720px}
.chips{position:absolute;left:72px;right:72px;bottom:96px;display:flex;flex-wrap:wrap;gap:12px}
.chips span{display:inline-flex;align-items:center;gap:10px;height:42px;padding:0 18px;border-radius:999px;font-size:19px;font-weight:600;background:#111924;border:1px solid #273444}
.chips i{width:11px;height:11px;border-radius:50%;background:var(--c)}
.url{position:absolute;left:72px;bottom:46px;font-size:18px;color:#9faebe}'''
    orbit = ('<svg class="orbit" viewBox="0 0 460 460" fill="none"><circle cx="230" cy="230" r="200" stroke="#273444"/>'
             '<circle cx="230" cy="230" r="150" stroke="#273444" stroke-dasharray="3 8"/>'
             '<ellipse cx="230" cy="230" rx="215" ry="90" stroke="#1d2a3a" transform="rotate(-35 230 230)"/>'
             '<ellipse cx="230" cy="230" rx="215" ry="90" stroke="#1d2a3a" transform="rotate(35 230 230)"/>'
             '<circle cx="230" cy="230" r="62" fill="#111924" stroke="#b8ee91" stroke-opacity=".5"/>'
             '<text x="230" y="243" text-anchor="middle" fill="#eaf0f6" font-size="36" font-weight="700" font-family="ui-monospace,Menlo">LW</text></svg>')
    body = (f'<div class="glow"></div>{orbit}<div class="eyebrow"><b>LW</b>LEON WANG · AI APPLICATIONS &amp; RESEARCH</div>'
            '<h1>Exploring intelligence.<br><span>Sharing understanding.</span></h1>'
            '<p class="sub">MSc student at The University of Hong Kong. Applied AI projects with live demos, '
            'AAAI 2025 research on long-video grounding, and a bilingual learning hub.</p>'
            f'<div class="chips">{chips}</div><div class="url mono">leon1111-wgl.github.io/leon1111-wgl</div>')
    return page(w, h, css, body)


def map_svg(data, width):
    courses = {c['id']: c for c in data['courses']}
    order = [cid for r in data['route'] for cid in r['courses']]
    road = smooth([MAP[c] for c in order])
    houses = ''.join(
        f'<g transform="translate({MAP[c][0]} {MAP[c][1]})"><ellipse cx="0" cy="4" rx="20" ry="5" fill="#000" opacity=".45"/>'
        f'<rect x="-13" y="-15" width="26" height="18" rx="2.5" fill="#141823" stroke="{courses[c]["color"]}" stroke-width="1.6"/>'
        f'<path d="M-17 -13L0 -29L17 -13Z" fill="{courses[c]["color"]}"/><rect x="-3" y="-7" width="6" height="10" rx="1.2" fill="#ffe9a3" opacity=".85"/>'
        f'<text y="23" text-anchor="middle" font-size="14" font-weight="600" fill="#eceef2">{E(courses[c]["short"]["zh"])}</text></g>'
        for c in order)
    return (f'<svg width="{width}" viewBox="10 20 620 440" fill="none">'
            '<path d="M250 0C232 80 304 140 282 214c-20 76 44 130 20 256" stroke="rgb(76 155 255 / 22%)" stroke-width="13" stroke-linecap="round"/>'
            f'<path d="{road}" stroke="#07080c" stroke-width="15" stroke-linecap="round"/><path d="{road}" stroke="#2a3040" stroke-width="10" stroke-linecap="round"/>'
            f'<path d="{road}" stroke="rgb(255 255 255 / 45%)" stroke-width="1.4" stroke-dasharray="6 9"/>{houses}</svg>')


def learn_card(w, h):
    data = catalogue(); t = data['totals']
    css = '''body{background:#0b0d12;color:#eceef2;position:relative;padding:60px 64px}
.bg{position:absolute;inset:0;background:radial-gradient(ellipse 45% 45% at 78% 20%,rgb(30 107 255/.22),transparent 70%),radial-gradient(ellipse 35% 35% at 96% 85%,rgb(192 132 252/.16),transparent 70%),linear-gradient(90deg,rgb(255 255 255/.04) 1px,transparent 1px) 0 0/64px 64px,linear-gradient(rgb(255 255 255/.04) 1px,transparent 1px) 0 0/64px 64px}
.brand{position:relative;display:flex;align-items:center;gap:14px;font-size:24px;font-weight:700}
.brand b{display:grid;place-items:center;width:44px;height:44px;border-radius:12px;background:#1e6bff;color:#fff;font:700 17px/1 ui-monospace,Menlo,monospace}
.brand small{font-size:19px;font-weight:500;color:#8d95a3}
h1{position:relative;margin-top:50px;font-size:74px;line-height:1.12;font-weight:800;letter-spacing:2px}
h1 span{display:inline-block;margin-top:12px;padding:0 22px 8px;border-radius:18px;color:#fff;background:linear-gradient(100deg,#1e6bff,#6d5dfc 55%,#c084fc)}
p.en{position:relative;margin-top:26px;font-size:24px;color:#b9bfca}
p.subjects{position:relative;margin-top:10px;font-size:20px;color:#8d95a3}
.stats{position:absolute;left:64px;bottom:54px;display:flex;gap:34px}
.stats div{font-size:18px;color:#8d95a3}.stats b{display:block;font-size:38px;line-height:1.1;color:#eceef2;font-weight:700}
.map{position:absolute;right:40px;top:96px;width:560px;height:440px;border-radius:22px;background:#12151c;border:1px solid #303644;overflow:hidden;box-shadow:0 40px 90px -40px rgb(30 107 255/.5)}
.map svg{display:block}'''
    body = ('<div class="bg"></div><div class="brand"><b>LW</b>Leon 学习 <small>Leon Learn · 学习中心</small></div>'
            '<h1>从零学会编程<br><span>中英双语</span></h1>'
            '<p class="en">Learn to code from zero, in Chinese and English.</p>'
            '<p class="subjects">Python · Java · C · 算法 · 计算理论 · AI</p>'
            f'<div class="stats"><div><b>{t["courses"]}</b>门课程与路线</div><div><b>{t["chapters"]}</b>章</div><div><b>{t["programs"]}</b>份可运行代码</div></div>'
            f'<div class="map">{map_svg(data, 560)}</div>')
    return page(w, h, css, body)


# One identity per project, from the design registry: background, ink, muted ink, accent, line, and a motif.
STYLES = {
    'loopdesk': dict(bg='#0b0d12', ink='#eceef2', muted='#8d95a3', accent='#4c9bff', line='#303644', panel='#12151c', font='sans'),
    'proofbi': dict(bg='#0f171a', ink='#e4efec', muted='#9db3ae', accent='#46c79c', line='#21343a', panel='#13201f', font='sans'),
    'adproof': dict(bg='#f4ece8', ink='#2b2520', muted='#6d625a', accent='#b93a22', line='#e2d3cb', panel='#fbf6f3', font='serif'),
    'creditlens': dict(bg='#0b1026', ink='#e8eaf6', muted='#a3a9c9', accent='#ad9bff', line='#2a3260', panel='#131a3a', font='sans'),
    'estateguard': dict(bg='#121310', ink='#ecebe4', muted='#a9a79b', accent='#eea935', line='#2f2f28', panel='#1a1b17', font='sans'),
    'finscope': dict(bg='#0e1612', ink='#ede4cf', muted='#b3ab97', accent='#22c3d6', line='#26352d', panel='#13201a', font='serif'),
}


def motif(pid, s):
    a, line, panel, ink, muted = s['accent'], s['line'], s['panel'], s['ink'], s['muted']
    if pid == 'loopdesk':  # a reply with evidence marks, and a refund that waits for a person
        return (f'<svg viewBox="0 0 420 420" fill="none"><rect x="20" y="40" width="250" height="64" rx="18" fill="{panel}" stroke="{line}"/>'
                f'<rect x="44" y="62" width="170" height="8" rx="4" fill="{muted}" opacity=".6"/><rect x="44" y="80" width="120" height="8" rx="4" fill="{muted}" opacity=".4"/>'
                f'<rect x="120" y="128" width="280" height="96" rx="18" fill="{a}" fill-opacity=".14" stroke="{a}" stroke-opacity=".5"/>'
                f'<rect x="144" y="152" width="200" height="8" rx="4" fill="{ink}" opacity=".75"/><rect x="144" y="170" width="160" height="8" rx="4" fill="{ink}" opacity=".55"/>'
                f'<rect x="144" y="194" width="34" height="16" rx="5" fill="{a}"/><rect x="186" y="194" width="34" height="16" rx="5" fill="{a}" opacity=".6"/>'
                f'<rect x="60" y="256" width="340" height="132" rx="18" fill="{panel}" stroke="{line}"/><circle cx="96" cy="296" r="14" stroke="{a}" stroke-width="2.5"/>'
                f'<path d="M96 288v9l6 4" stroke="{a}" stroke-width="2.5" stroke-linecap="round"/><rect x="124" y="288" width="150" height="9" rx="4.5" fill="{ink}" opacity=".7"/>'
                f'<rect x="124" y="305" width="100" height="8" rx="4" fill="{muted}" opacity=".5"/><rect x="84" y="336" width="140" height="34" rx="17" fill="{a}"/>'
                f'<path d="M136 353l8 8 16-16" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/><rect x="236" y="336" width="140" height="34" rx="17" stroke="{line}" stroke-width="1.5"/></svg>')
    if pid == 'proofbi':  # question -> metric -> SQL -> number on drafting paper, the lit path in jade
        nodes = [('Question', 60), ('Metric', 150), ('SQL', 240), ('Number', 330)]
        dots = ''.join(f'<circle cx="80" cy="{y}" r="11" fill="{s["bg"]}" stroke="{a}" stroke-width="3"/><circle cx="80" cy="{y}" r="4.5" fill="{a}"/>'
                       f'<rect x="116" y="{y - 24}" width="270" height="48" rx="8" fill="{panel}" stroke="{line}"/>'
                       f'<text x="136" y="{y + 7}" font-size="20" fill="{ink}" font-family="ui-monospace,Menlo">{n}</text>' for n, y in nodes)
        return (f'<svg viewBox="0 0 420 420" fill="none"><path d="M80 60V330" stroke="{a}" stroke-width="3" stroke-dasharray="7 7"/>{dots}'
                f'<rect x="300" y="314" width="70" height="32" rx="6" fill="{a}" fill-opacity=".18" stroke="{a}"/></svg>')
    if pid == 'adproof':  # a ruled manuscript with a struck claim, a circled number and a margin note
        lines = ''.join(f'<rect x="40" y="{y}" width="{w}" height="9" rx="4.5" fill="{ink}" opacity=".55"/>' for y, w in [(70, 250), (110, 230), (190, 210), (230, 240), (270, 180)])
        return (f'<svg viewBox="0 0 420 420" fill="none"><rect x="14" y="30" width="392" height="340" rx="10" fill="{panel}" stroke="{line}"/>'
                + ''.join(f'<path d="M30 {y}H390" stroke="{line}"/>' for y in range(90, 370, 40)) + lines +
                f'<rect x="40" y="150" width="200" height="9" rx="4.5" fill="{ink}" opacity=".55"/><path d="M36 155H246" stroke="{a}" stroke-width="3"/>'
                f'<path d="M40 170q12 8 24 0t24 0 24 0 24 0 24 0 24 0 24 0 24 0" stroke="{a}" stroke-width="2.2"/>'
                f'<circle cx="270" cy="154" r="15" stroke="{a}" stroke-width="2.5"/><text x="270" y="161" text-anchor="middle" font-size="18" fill="{a}" font-family="Georgia">1</text>'
                f'<path d="M286 154H322" stroke="{a}" stroke-dasharray="4 4"/><rect x="326" y="128" width="64" height="54" rx="6" fill="{s["bg"]}" stroke="{a}"/>'
                f'<text x="358" y="161" text-anchor="middle" font-size="20" fill="#1f4f8a" font-family="Georgia">§</text>'
                f'<text x="252" y="246" font-size="30" fill="#1f4f8a" font-family="Georgia">‸</text></svg>')
    if pid == 'creditlens':  # a filing table read through a brass loupe, with the readout fields underneath
        rows = ''.join(f'<path d="M30 {y}H390" stroke="{line}"/><rect x="40" y="{y + 14}" width="120" height="8" rx="4" fill="{muted}" opacity=".55"/>'
                       f'<rect x="250" y="{y + 14}" width="{60 + (y % 3) * 14}" height="8" rx="4" fill="{ink}" opacity=".55"/>' for y in range(60, 300, 40))
        return (f'<svg viewBox="0 0 420 420" fill="none"><rect x="20" y="30" width="380" height="290" rx="12" fill="{panel}" stroke="{line}"/>{rows}'
                f'<circle cx="290" cy="178" r="62" fill="{s["bg"]}" fill-opacity=".55" stroke="#d5ac5f" stroke-width="6"/><rect x="252" y="172" width="78" height="12" rx="6" fill="{a}"/>'
                f'<path d="M335 224l44 44" stroke="#d5ac5f" stroke-width="12" stroke-linecap="round"/>'
                f'<text x="24" y="368" font-size="17" fill="#d5ac5f" font-family="ui-monospace,Menlo">value · page · bbox · unit</text></svg>')
    if pid == 'estateguard':  # a site plan with cameras, amber fields of view and a corner-bracket box
        blocks = ''.join(f'<rect x="{x}" y="{y}" width="{w}" height="{hh}" rx="4" fill="{panel}" stroke="{line}"/>' for x, y, w, hh in [(30, 40, 150, 110), (210, 40, 180, 80), (30, 190, 110, 170), (250, 200, 140, 160)])
        cams = ''.join(f'<path d="M{x} {y}L{x + dx} {y - 70}L{x + dx + 60} {y - 40}Z" fill="{a}" fill-opacity=".18"/><circle cx="{x}" cy="{y}" r="7" fill="{a}"/>' for x, y, dx in [(190, 175, -10), (230, 330, 10), (160, 380, -60)])
        br = '#4cc3b8'
        return (f'<svg viewBox="0 0 420 420" fill="none"><rect x="10" y="20" width="400" height="380" rx="12" stroke="{line}"/>{blocks}'
                f'<path d="M150 170H400M190 30V400" stroke="{line}" stroke-width="10" opacity=".7"/>{cams}'
                f'<path d="M262 236v-16h16M362 220h16v16M378 312v16h-16M278 328h-16v-16" stroke="{br}" stroke-width="3"/></svg>')
    if pid == 'finscope':  # the water line: cash as a water level, profit drawn over it, red hatching where profit stands above cash
        return (f'<svg viewBox="0 0 420 420" fill="none"><defs><pattern id="hatch" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
                f'<path d="M0 0V8" stroke="#ef8a72" stroke-width="2"/></pattern></defs><rect x="20" y="30" width="380" height="340" rx="10" fill="{panel}" stroke="{line}"/>'
                f'<path d="M40 250C90 230 120 240 160 220S240 210 280 236 350 250 380 240V350H40Z" fill="{a}" fill-opacity=".22"/>'
                f'<path d="M40 250C90 230 120 240 160 220S240 210 280 236 350 250 380 240" stroke="{a}" stroke-width="3"/>'
                f'<path d="M280 236C300 200 330 170 380 150V240C350 250 310 246 280 236Z" fill="url(#hatch)" opacity=".8"/>'
                f'<path d="M40 270C100 250 160 230 220 228S300 214 380 150" stroke="{ink}" stroke-width="2.5" stroke-dasharray="1 0"/>'
                f'<path d="M40 360H380M40 364H380" stroke="#d9b45a" stroke-width="1.5"/></svg>')
    return ''


def repo_card(p, w, h):
    s = STYLES[p['id']]
    serif = s['font'] == 'serif'
    css = f'''body{{background:{s["bg"]};color:{s["ink"]};position:relative;padding:64px 72px}}
.eyebrow{{font-size:18px;letter-spacing:2.5px;color:{s["accent"]};text-transform:uppercase}}
h1{{margin-top:22px;font-size:84px;line-height:1;font-weight:800;letter-spacing:-1.5px;{'font-family:Georgia,"Songti SC",serif;font-weight:700;' if serif else ''}}}
p.en{{margin-top:26px;max-width:700px;font-size:30px;line-height:1.35;font-weight:600}}
p.zh{{margin-top:16px;max-width:700px;font-size:24px;line-height:1.55;color:{s["muted"]}}}
ul{{list-style:none;padding:0;margin-top:30px;display:flex;flex-wrap:wrap;gap:10px;max-width:720px}}
li{{padding:8px 16px;border-radius:999px;font-size:18px;border:1px solid {s["line"]};background:{s["panel"]}}}
.note{{position:absolute;left:72px;bottom:96px;max-width:720px;font-size:17px;line-height:1.5;color:{s["muted"]}}}
.url{{position:absolute;left:72px;bottom:50px;font-size:19px;color:{s["accent"]}}}
.motif{{position:absolute;right:56px;top:110px;width:420px;height:420px}}
.rule{{position:absolute;left:0;right:0;top:0;height:6px;background:{s["accent"]}}}'''
    body = (f'<div class="rule"></div><div class="eyebrow">Leon Wang · {E(p["tag"])}</div><h1>{E(p["name"])}</h1>'
            f'<p class="en">{E(p["en"])}</p><p class="zh">{E(p["zh"])}</p><ul>{"".join(f"<li>{E(x)}</li>" for x in p["stack"])}</ul>'
            f'<p class="note">{E(p["note"])}</p><div class="url mono">leon1111-wgl.github.io/{p["id"]}</div>'
            f'<div class="motif">{motif(p["id"], s)}</div>')
    return page(w, h, css, body)


def render(html, out, w, h):
    """Screenshot one card with headless Chrome at exactly w x h pixels."""
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / 'card.html'
        src.write_text(html)
        subprocess.run([CHROME, '--headless', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=1',
                        f'--window-size={w},{h}', f'--screenshot={out}', f'--user-data-dir={tmp}/profile', src.as_uri()],
                       check=True, capture_output=True, timeout=120)


def images():
    if not Path(CHROME).exists():
        sys.exit('Google Chrome is needed to draw the share cards; the committed PNGs are unchanged.')
    OG.mkdir(parents=True, exist_ok=True)
    cards = [('home.png', home_card, 1200, 630), ('learn.png', learn_card, 1200, 630),
             ('repo-leon1111-wgl.png', home_card, 1280, 640)]
    for p in project_list():
        cards.append((f'repo-{p["id"]}.png', lambda w, h, p=p: repo_card(p, w, h), 1280, 640))
    for name, make, w, h in cards:
        render(make(w, h), OG / name, w, h)
    return [c[0] for c in cards]


if __name__ == '__main__':
    print(f'sitemap.xml: {sitemap()} URLs; robots.txt written')
    if '--images' in sys.argv:
        print('share cards:', ', '.join(images()))
