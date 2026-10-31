"""Write site/assets/profile-background.svg: experience, education and research as one animated panel.

One 12 s cycle drives the whole panel: a light runs along the experience timeline, sweeps down
into education, then into research, so the three sections read as one sequence.
"""
import math
from pathlib import Path

W, H, CYCLE = 840, 700, 12.0
CJK = "'PingFang SC','Hiragino Sans GB','Microsoft YaHei','Noto Sans SC',Arial,sans-serif"


def pulse(t, base=".15", peak="1", rest=".35", hold=1.5):
    k = t / CYCLE
    a, c = max(k - .02, .001), min(k + hold / CYCLE, .999)
    return (f'<animate attributeName="opacity" values="{base};{base};{peak};{rest};{base}" '
            f'keyTimes="0;{a:.3f};{k:.3f};{c:.3f};1" dur="{CYCLE:g}s" repeatCount="indefinite"/>')


def sweep(y, t0, t1):
    a, b = t0 / CYCLE, t1 / CYCLE
    return (f'<line x1="23" y1="{y}" x2="817" y2="{y}" stroke="#1f2f3e"/>'
            f'<rect x="-140" y="{y - 1}" width="140" height="2" fill="url(#sweep)">'
            f'<animate attributeName="x" values="-140;-140;840;840" keyTimes="0;{a:.3f};{b:.3f};1" '
            f'dur="{CYCLE:g}s" repeatCount="indefinite"/></rect>')


def card(x, y, w, h, t, dashed=False):
    dash = ' stroke-dasharray="4 4"' if dashed else ''
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#0f1824" stroke="#1f2f3e"{dash}/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="2.5" rx="1.2" fill="#60c9ce">{pulse(t)}</rect>')


def experience():
    nodes = [
        (120, "深圳北斗应用技术研究院", "Beidou Institute · 深圳", "AI Algorithm Intern", ["华润物业视频异常事件检测"]),
        (320, "华夏银行（分行）", "Hua Xia Bank · Branch", "Intern", ["授信尽调智能助手（Agent）", "对接客户需求"]),
        (520, "中国科学院研究所", "CAS · 北京", "研究中", []),
        (720, "中国科学院深圳先进技术研究院", "SIAT, CAS · 深圳", "研究中", []),
    ]
    out = ['<text x="36" y="40" class="label">EXPERIENCE</text>',
           '<line x1="70" y1="96" x2="770" y2="96" stroke="#2a3b4b" stroke-width="2"/>']
    for i, (x, org, en, role, desc) in enumerate(nodes):
        t = (x - 70) / 100
        out += [f'<text x="{x}" y="76" text-anchor="middle" class="step">0{i + 1}</text>',
                f'<circle class="ring" cx="{x}" cy="96" r="7" fill="none" stroke="#60c9ce" style="animation-delay:{t:g}s"/>',
                f'<circle cx="{x}" cy="96" r="7" fill="#101d29" stroke="#60c9ce" stroke-width="1.5"/>',
                f'<circle cx="{x}" cy="96" r="3.2" fill="#b8ee91">{pulse(t, ".25", "1", ".45")}</circle>',
                card(x - 97, 118, 194, 132, t),
                f'<text x="{x}" y="146" text-anchor="middle" class="org">{org}</text>',
                f'<text x="{x}" y="166" text-anchor="middle" class="en">{en}</text>',
                f'<text x="{x}" y="191" text-anchor="middle" class="role">{role}</text>']
        out += [f'<text x="{x}" y="{214 + 19 * j}" text-anchor="middle" class="desc">{d}</text>' for j, d in enumerate(desc)]
    move = f'dur="{CYCLE:g}s" repeatCount="indefinite"'
    fade = f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.575;.6;1" {move}/>'
    out += [f'<rect x="10" y="94.5" width="60" height="3" rx="1.5" fill="url(#trail)">'
            f'<animate attributeName="x" values="10;710;710" keyTimes="0;.583;1" {move}/>{fade}</rect>',
            f'<circle cx="70" cy="96" r="4" fill="#b8ee91">'
            f'<animate attributeName="cx" values="70;770;770" keyTimes="0;.583;1" {move}/>{fade}</circle>']
    return out


def shield(cx, cy):
    return (f'M{cx - 15} {cy - 17}H{cx + 15}V{cy - 2}C{cx + 15} {cy + 10} {cx + 6} {cy + 16} {cx} {cy + 19}'
            f'C{cx - 6} {cy + 16} {cx - 15} {cy + 10} {cx - 15} {cy - 2}Z')


def emblem(kind, cx, cy, t):
    # Stylised emblems in each university's colours, not the official crests.
    out = [f'<circle cx="{cx}" cy="{cy}" r="27" fill="#101d29" stroke="#2a3b4b"/>',
           f'<circle cx="{cx}" cy="{cy}" r="27" fill="none" stroke="#b8ee91" stroke-width="1.2">{pulse(t, "0", ".9", "0")}</circle>',
           f'<circle class="spin" style="transform-origin:{cx}px {cy}px" cx="{cx}" cy="{cy}" r="32" fill="none" '
           f'stroke="#527e86" stroke-dasharray="2 7"/>']
    if kind == "hku":
        out += [f'<path d="{shield(cx, cy)}" fill="#00573f" fill-opacity=".55" stroke="#4fc79a" stroke-width="1.3"/>',
                f'<line x1="{cx - 15}" y1="{cy - 9}" x2="{cx + 15}" y2="{cy - 9}" stroke="#4fc79a" stroke-opacity=".7"/>',
                f'<text x="{cx}" y="{cy + 6}" text-anchor="middle" class="mono">HKU</text>']
    elif kind == "usyd":
        stars = ''.join(f'<circle cx="{cx + dx}" cy="{cy + dy}" r="1.1" fill="#f3a183"/>'
                        for dx, dy in ((-6, -13), (0, -14.5), (6, -12.5), (1, -11)))
        out += [f'<path d="{shield(cx, cy)}" fill="#e64626" fill-opacity=".22" stroke="#f0805f" stroke-width="1.3"/>',
                f'<line x1="{cx - 15}" y1="{cy - 9}" x2="{cx + 15}" y2="{cy - 9}" stroke="#f0805f" stroke-opacity=".7"/>',
                stars, f'<text x="{cx}" y="{cy + 6}" text-anchor="middle" class="mono" font-size="8.5">USYD</text>']
    else:
        out += [f'<circle cx="{cx}" cy="{cy}" r="17.5" fill="#1e5bb8" fill-opacity=".28" stroke="#79a6f2" stroke-width="1.3"/>',
                f'<circle cx="{cx}" cy="{cy}" r="13.5" fill="none" stroke="#79a6f2" stroke-opacity=".6" stroke-dasharray="1.5 2.5"/>',
                f'<text x="{cx}" y="{cy + 3.5}" text-anchor="middle" class="mono">ZJU</text>']
    return out


def education():
    schools = [
        ("hku", "香港大学", "The University of Hong Kong", "MSc · 2026 –", "理学硕士"),
        ("usyd", "悉尼大学", "The University of Sydney", "Finance &amp; Computer Science", "金融与计算机科学 · Dalyell 学者"),
        ("zju", "浙江大学", "Zhejiang University", "Short-term exchange", "短期交流"),
    ]
    out = [sweep(272, 6.9, 7.7), '<text x="36" y="312" class="label">EDUCATION</text>']
    for i, (kind, zh, en, role, desc) in enumerate(schools):
        x, t = 23 + 270 * i, 7.6 + .6 * i
        cx = x + 126
        out += [card(x, 330, 252, 166, t), *emblem(kind, cx, 370, t),
                f'<text x="{cx}" y="422" text-anchor="middle" class="org">{zh}</text>',
                f'<text x="{cx}" y="440" text-anchor="middle" class="en">{en}</text>',
                f'<text x="{cx}" y="461" text-anchor="middle" class="role">{role}</text>',
                f'<text x="{cx}" y="480" text-anchor="middle" class="desc">{desc}</text>']
    return out


def cube_icon(cx, cy):
    # A wireframe cube turning about its vertical axis; a quarter turn maps the cube onto itself, so the loop is seamless.
    verts = [(x, y, z) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]
    edges = [(a, b) for a in range(8) for b in range(a + 1, 8) if sum(p != q for p, q in zip(verts[a], verts[b])) == 1]
    tilt, s = math.radians(24), 9.5

    def frame(theta):
        pts = []
        for x, y, z in verts:
            xr, zr = x * math.cos(theta) + z * math.sin(theta), -x * math.sin(theta) + z * math.cos(theta)
            pts.append((cx + s * xr, cy + s * (y * math.cos(tilt) - zr * math.sin(tilt))))
        return ''.join(f'M{pts[a][0]:.1f} {pts[a][1]:.1f}L{pts[b][0]:.1f} {pts[b][1]:.1f}' for a, b in edges)

    frames = [frame(math.radians(90 * k / 12)) for k in range(13)]
    return [f'<ellipse cx="{cx}" cy="{cy + 17}" rx="15" ry="3.5" fill="none" stroke="#2a3b4b"/>',
            f'<path d="{frames[0]}" fill="none" stroke="#60c9ce" stroke-width="1.2" stroke-linejoin="round">'
            f'<animate attributeName="d" values="{";".join(frames)}" dur="6s" repeatCount="indefinite"/></path>',
            f'<circle cx="{cx}" cy="{cy}" r="2" fill="#b8ee91"/>']


def film_icon(cx, cy):
    frames = ''.join(f'<rect x="{cx - 20 + 7 * i}" y="{cy - 11}" width="5.5" height="13" rx="1" fill="#142130" stroke="#2a3b4b"/>'
                     for i in range(6))
    return [frames,
            f'<rect x="{cx - 21.5}" y="{cy - 13}" width="15.5" height="17" rx="2" fill="#b8ee91" fill-opacity=".14" stroke="#b8ee91" stroke-width="1.2">'
            f'<animate attributeName="x" values="{cx - 21.5};{cx + 5.5};{cx - 7.5};{cx - 21.5}" keyTimes="0;.4;.7;1" dur="5s" repeatCount="indefinite" '
            f'calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1;.45 0 .55 1"/></rect>',
            f'<line x1="{cx - 20}" y1="{cy + 12}" x2="{cx + 20}" y2="{cy + 12}" stroke="#2a3b4b" stroke-width="2"/>',
            f'<circle cx="{cx - 20}" cy="{cy + 12}" r="2.4" fill="#60c9ce">'
            f'<animate attributeName="cx" values="{cx - 20};{cx + 20}" dur="5s" repeatCount="indefinite"/></circle>']


def arm_icon(cx, cy):
    rot = 'attributeName="transform" type="rotate" dur="4.5s" repeatCount="indefinite" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1"'
    return [f'<path d="M{cx - 17} {cy + 18}H{cx - 3}L{cx - 6} {cy + 13}H{cx - 14}Z" fill="#142130" stroke="#527e86"/>',
            f'<g transform="translate({cx - 10} {cy + 12})"><g>'
            f'<animateTransform {rot} values="-62;-38;-62" keyTimes="0;.5;1"/>'
            f'<line x1="0" y1="0" x2="15" y2="0" stroke="#60c9ce" stroke-width="2.2" stroke-linecap="round"/>'
            f'<circle r="2.6" fill="#101d29" stroke="#60c9ce"/>'
            f'<g transform="translate(15 0)"><g><animateTransform {rot} values="78;40;78" keyTimes="0;.5;1"/>'
            f'<line x1="0" y1="0" x2="12" y2="0" stroke="#60c9ce" stroke-width="2" stroke-linecap="round"/>'
            f'<circle r="2.3" fill="#101d29" stroke="#60c9ce"/>'
            f'<path d="M12 -4L16 -4M12 4L16 4M12 -4V4" fill="none" stroke="#b8ee91" stroke-width="1.4"/>'
            f'</g></g></g></g>']


def graph_icon(cx, cy):
    sats = [(cx - 14, cy - 12), (cx + 15, cy - 9), (cx + 2, cy + 16)]
    out = []
    for i, (x, y) in enumerate(sats):
        out += [f'<line x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" stroke="#527e86" stroke-dasharray="2 3">'
                f'<animate attributeName="stroke-dashoffset" values="10;0" dur="1.2s" repeatCount="indefinite"/></line>',
                f'<circle cx="{x}" cy="{y}" r="3.4" fill="#101d29" stroke="#60c9ce"/>',
                f'<circle cx="{x}" cy="{y}" r="1.6" fill="#b8ee91" opacity=".2">'
                f'<animate attributeName="opacity" values=".2;1;.2;.2" keyTimes="0;{.1 + .3 * i:.1f};{.25 + .3 * i:.2f};1" dur="3s" repeatCount="indefinite"/></circle>']
    return out + [f'<circle cx="{cx}" cy="{cy}" r="5.5" fill="#101d29" stroke="#b8ee91" stroke-width="1.4"/>',
                  f'<circle cx="{cx}" cy="{cy}" r="2" fill="#b8ee91"/>']


def research():
    areas = [
        (cube_icon, "空间智能", "Spatial Intelligence", False),
        (film_icon, "多模态长视频理解与定位", "Long-video Grounding", False),
        (arm_icon, "具身智能（未来）", "Embodied AI · next", True),
        (graph_icon, "企业级 Agent 应用与开发", "Enterprise AI Agents", False),
    ]
    out = [sweep(512, 9.0, 9.8), '<text x="36" y="548" class="label">RESEARCH</text>']
    for i, (icon, zh, en, future) in enumerate(areas):
        x, t = 23 + 202 * i, 9.8 + .5 * i
        cx = x + 40
        out += [card(x, 564, 188, 112, t, dashed=future),
                f'<g transform="translate({cx} 600) scale(1.25) translate({-cx} -600)">', *icon(cx, 600), '</g>',
                f'<text x="{x + 172}" y="590" text-anchor="end" class="step">0{i + 1}</text>',
                f'<text x="{x + 16}" y="645" class="org">{zh}</text>',
                f'<text x="{x + 16}" y="663" class="en">{en}</text>']
    return out


TITLE = ("Background. Experience, oldest first: AI Algorithm Intern at Beidou Institute, Shenzhen, video anomaly event "
         "detection for China Resources property management; Intern at Hua Xia Bank (branch), credit due-diligence "
         "assistant agent and client requirements; ongoing research at the Chinese Academy of Sciences, Beijing, and at Shenzhen "
         "Institutes of Advanced Technology, CAS. Education: The University of Hong Kong, MSc, 2026 onwards; The University "
         "of Sydney, Finance and Computer Science, Dalyell Scholar; Zhejiang University, short-term exchange. Research: "
         "spatial intelligence; multimodal long-video understanding and grounding; embodied AI (future); enterprise AI agents.")

STYLE = f"""
  .label {{ font: 700 13px Arial, sans-serif; fill: #60c9ce; letter-spacing: 3px; }}
  .step {{ font: 12px monospace; fill: #527e86; }}
  .org {{ font: 700 13.5px {CJK}; fill: #f2f6fb; }}
  .en {{ font: 12px Arial, sans-serif; fill: #8aa0b4; }}
  .role {{ font: 700 13px Arial, {CJK}; fill: #b8ee91; }}
  .desc {{ font: 12.5px {CJK}; fill: #c4d0dc; }}
  .mono {{ font: 700 10px Arial, sans-serif; fill: #f2f6fb; letter-spacing: .5px; }}
  .ring {{ animation: ring 2.6s ease-out infinite; transform-box: fill-box; transform-origin: center; }}
  @keyframes ring {{ 0% {{ opacity: .7; transform: scale(1); }} 100% {{ opacity: 0; transform: scale(2.4); }} }}
  .spin {{ animation: spin 24s linear infinite; }}
  @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
  @media (prefers-reduced-motion: reduce) {{ .ring {{ animation: none; opacity: 0; }} .spin {{ animation: none; }} }}
"""


def build():
    body = experience() + education() + research()
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">
<title id="t">{TITLE}</title>
<style>{STYLE}</style>
<defs>
  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#1d2b3a" stroke-width=".7"/></pattern>
  <linearGradient id="trail" x1="0" x2="1"><stop offset="0" stop-color="#b8ee91" stop-opacity="0"/><stop offset="1" stop-color="#b8ee91" stop-opacity=".9"/></linearGradient>
  <linearGradient id="sweep" x1="0" x2="1"><stop offset="0" stop-color="#60c9ce" stop-opacity="0"/><stop offset=".7" stop-color="#b8ee91" stop-opacity=".9"/><stop offset="1" stop-color="#b8ee91" stop-opacity="0"/></linearGradient>
  <clipPath id="round"><rect width="{W}" height="{H}" rx="18"/></clipPath>
</defs>
<g clip-path="url(#round)">
<rect width="{W}" height="{H}" fill="#0b111c"/><rect width="{W}" height="{H}" fill="url(#grid)"/>
{chr(10).join(body)}
</g>
</svg>
"""
    out = Path(__file__).resolve().parents[1] / "site" / "assets" / "profile-background.svg"
    out.write_text(svg, encoding="utf-8")
    print(out, len(svg))


if __name__ == "__main__":
    build()
