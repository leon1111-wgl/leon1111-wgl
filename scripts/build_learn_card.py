"""Write the README card that links to the learning hub (site/assets/profile-learn.svg).

The right half is a small copy of the hub's learning map: one coloured house per course,
joined by a road in the suggested order, with a light travelling along it.
"""
from pathlib import Path

from build_learn import MAP, catalogue
from palette import COURSE_COLORS

ROOT = Path(__file__).resolve().parents[1]

def smooth(points):
    """A Catmull-Rom curve through the points, written as cubic Béziers."""
    d = f'M{points[0][0]:.1f} {points[0][1]:.1f}'
    for i in range(len(points) - 1):
        p0 = points[i - 1] if i else points[i]
        p1, p2 = points[i], points[i + 1]
        p3 = points[i + 2] if i + 2 < len(points) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f' C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}'
    return d


def map_svg(base=''):
    """The learning map at full size for the homepage: each house links to its course in the hub."""
    data = catalogue()
    courses = {c['id']: c for c in data['courses']}
    order = [cid for r in data['route'] for cid in r['courses']]
    road = smooth([MAP[c] for c in order])
    houses = ''.join(
        f'<a href="{base}learn/#/course/{c}" class="hm-house" style="--c:{COURSE_COLORS[c]}">'
        f'<title>{courses[c]["short"]["en"]} · {courses[c]["short"]["zh"]}</title>'
        f'<g transform="translate({x} {y})"><rect x="-11" y="-12" width="22" height="15" rx="2"/>'
        f'<path d="M-14.5 -11L0 -24L14.5 -11Z"/><rect class="hm-door" x="-2.5" y="-6" width="5" height="9" rx="1"/>'
        f'<text y="20" text-anchor="middle">{courses[c]["short"]["en"]}</text></g></a>'
        for c, (x, y) in ((c, MAP[c]) for c in order))
    return (f'<svg class="hub-map" viewBox="30 40 600 410" role="group" aria-label="Learning map: one house per course, joined in the suggested order">'
            f'<path class="hm-river" d="M250 40C232 120 304 180 282 254S326 384 302 450"/>'
            f'<path id="hm-road" class="hm-road" d="{road}"/><path class="hm-lane" d="{road}"/><path class="hm-flow" d="{road}"/>'
            f'<circle class="hm-mover" r="4"><animateMotion dur="16s" repeatCount="indefinite"><mpath href="#hm-road"/></animateMotion></circle>'
            f'{houses}</svg>')


def build():
    data = catalogue()
    order = [cid for r in data['route'] for cid in r['courses']]
    scale, ox, oy = 0.43, 548, 12
    place = {cid: (ox + x * scale, oy + y * scale) for cid, (x, y) in MAP.items()}
    road = smooth([place[c] for c in order])
    houses = ''.join(
        f'<g transform="translate({x:.1f} {y:.1f})"><rect x="-7" y="-8" width="14" height="10" rx="1.5" fill="#141823" stroke="{COURSE_COLORS[c]}"/>'
        f'<path d="M-9.5 -7.5L0 -16L9.5 -7.5Z" fill="{COURSE_COLORS[c]}"/><rect x="-1.6" y="-4" width="3.2" height="6" rx=".8" fill="#ffe9a3" opacity=".8"/></g>'
        for c, (x, y) in ((c, place[c]) for c in order))
    t = data['totals']
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="840" height="236" viewBox="0 0 840 236" role="img" aria-labelledby="t">
<title id="t">Leon 学习中心：中英双语编程与 AI 教程，{t['courses']} 门课程、{t['chapters']} 章、{t['programs']} 份可运行代码</title>
<style>
  .k {{ font: 700 11px Arial, Helvetica, sans-serif; letter-spacing: 2px; fill: #4c9bff; }}
  .h {{ font: 700 34px -apple-system, "PingFang SC", "Microsoft YaHei", Arial, sans-serif; fill: #eceef2; }}
  .s {{ font: 400 14px -apple-system, "PingFang SC", "Microsoft YaHei", Arial, sans-serif; fill: #9aa3b2; }}
  .n {{ font: 700 22px Arial, Helvetica, sans-serif; fill: #eceef2; }}
  .u {{ font: 400 12px -apple-system, "PingFang SC", "Microsoft YaHei", Arial, sans-serif; fill: #8d95a3; }}
  .b {{ font: 700 13px -apple-system, "PingFang SC", "Microsoft YaHei", Arial, sans-serif; fill: #fff; }}
  .line {{ fill: none; stroke: rgb(255 255 255 / 50%); stroke-width: 1; stroke-dasharray: 4 6; animation: flow 3s linear infinite; }}
  @keyframes flow {{ to {{ stroke-dashoffset: -40; }} }}
  @media (prefers-reduced-motion: reduce) {{ .line {{ animation: none; }} .mover {{ display: none; }} }}
</style>
<defs>
  <clipPath id="r"><rect width="840" height="236" rx="18"/></clipPath>
  <radialGradient id="g1" cx=".82" cy=".1" r=".55"><stop stop-color="#1e6bff" stop-opacity=".28"/><stop offset="1" stop-color="#1e6bff" stop-opacity="0"/></radialGradient>
  <radialGradient id="g2" cx=".98" cy=".9" r=".4"><stop stop-color="#c084fc" stop-opacity=".18"/><stop offset="1" stop-color="#c084fc" stop-opacity="0"/></radialGradient>
  <linearGradient id="btn" x1="0" x2="1"><stop stop-color="#1e6bff"/><stop offset=".6" stop-color="#6d5dfc"/><stop offset="1" stop-color="#c084fc"/></linearGradient>
  <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#1a1f2a" stroke-width=".7"/></pattern>
</defs>
<g clip-path="url(#r)">
  <rect width="840" height="236" fill="#0b0d12"/><rect width="840" height="236" fill="url(#grid)"/>
  <rect width="840" height="236" fill="url(#g1)"/><rect width="840" height="236" fill="url(#g2)"/>
  <rect x="530" y="10" width="296" height="216" rx="14" fill="#12151c" fill-opacity=".85" stroke="#262b37"/>
  <path d="M{ox + 250 * scale:.1f} {oy:.1f}C{ox + 232 * scale:.1f} {oy + 80 * scale:.1f} {ox + 304 * scale:.1f} {oy + 140 * scale:.1f} {ox + 282 * scale:.1f} {oy + 214 * scale:.1f}S{ox + 326 * scale:.1f} {oy + 344 * scale:.1f} {ox + 302 * scale:.1f} {oy + 470 * scale:.1f}" fill="none" stroke="rgb(76 155 255 / 22%)" stroke-width="6" stroke-linecap="round"/>
  <path id="road" d="{road}" fill="none" stroke="#07080c" stroke-width="8" stroke-linecap="round"/>
  <path d="{road}" fill="none" stroke="#2a3040" stroke-width="5.5" stroke-linecap="round"/>
  <path class="line" d="{road}"/>
  <circle class="mover" r="3" fill="#fff"><animateMotion dur="14s" repeatCount="indefinite"><mpath href="#road"/></animateMotion></circle>
  {houses}
  <text x="36" y="50" class="k">LEARNING HUB · 学习中心</text>
  <text x="36" y="94" class="h">从零学会编程，中英双语</text>
  <text x="36" y="122" class="s">Python · Java · C · 算法 · 计算理论 · 人工智能</text>
  <text x="36" y="168" class="n">{t['courses']}</text><text x="64" y="168" class="u">门课程</text>
  <text x="128" y="168" class="n">{t['chapters']}</text><text x="172" y="168" class="u">章</text>
  <text x="206" y="168" class="n">{t['programs']}</text><text x="250" y="168" class="u">份可运行代码</text>
  <rect x="36" y="186" width="150" height="34" rx="17" fill="url(#btn)"/>
  <text x="111" y="208" text-anchor="middle" class="b">进入学习中心 ↗</text>
</g>
</svg>
'''
    (ROOT / 'site' / 'assets' / 'profile-learn.svg').write_text(svg)
    print('profile-learn.svg written')


if __name__ == '__main__':
    build()
