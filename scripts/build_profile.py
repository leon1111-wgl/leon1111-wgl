#!/usr/bin/env python3
"""Build GitHub-compatible profile artwork and a personal-first README."""
from html import escape


def svg(body, width, height, title):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title">
<title id="title">{escape(title)}</title>
<defs><pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#253647" stroke-width=".65"/></pattern><radialGradient id="glow"><stop stop-color="#60c9ce" stop-opacity=".2"/><stop offset="1" stop-color="#0b111c" stop-opacity="0"/></radialGradient></defs>
<rect width="{width}" height="{height}" rx="18" fill="#0b111c"/>
<rect width="{width}" height="{height}" rx="18" fill="url(#grid)"/>
{body}</svg>'''


def artwork(root):
    assets = root / 'site' / 'assets'
    hero = '''<ellipse cx="1000" cy="180" rx="320" ry="280" fill="url(#glow)"/>
<path d="M40 70H1160" stroke="#2a3b4b"/>
<g fill="#b8ee91"><circle cx="46" cy="38" r="5"/><circle cx="66" cy="38" r="5" opacity=".55"/><circle cx="86" cy="38" r="5" opacity=".25"/></g>
<text x="1135" y="43" text-anchor="end" fill="#a6b7c8" font-family="monospace" font-size="13" letter-spacing="2">GUOLIANG / PERSONAL SPACE</text>
<text x="54" y="116" fill="#b8ee91" font-family="monospace" font-size="13" letter-spacing="3">AI RESEARCH · SYSTEMS · LEARNING</text>
<text x="49" y="204" fill="#f2f6fb" font-family="Arial,sans-serif" font-size="76" font-weight="700" letter-spacing="-3">Guoliang Wang</text>
<text x="54" y="253" fill="#b8ee91" font-family="Arial,sans-serif" font-size="25">MSc student @ HKU · Working on AI</text>
<text x="54" y="295" fill="#a6b7c8" font-family="Arial,sans-serif" font-size="21">Multimodal models. Long videos. Clear explanations.</text>
<g fill="none" stroke="#527e86"><circle cx="975" cy="222" r="126"/><circle cx="975" cy="222" r="88" stroke-dasharray="3 9"/><ellipse cx="975" cy="222" rx="152" ry="65" transform="rotate(-35 975 222)"/><path d="M898 122L1097 254L884 310L898 122M1097 254L975 222L898 122" opacity=".8"/></g>
<g fill="#b8ee91"><circle cx="898" cy="122" r="5"/><circle cx="1097" cy="254" r="5"/><circle cx="884" cy="310" r="5"/></g>
<circle cx="975" cy="222" r="44" fill="#101d29" stroke="#b8ee91"/>
<text x="975" y="232" text-anchor="middle" fill="#f2f6fb" font-family="monospace" font-size="27">GW</text>
<rect x="54" y="340" width="340" height="61" rx="9" fill="#b8ee91"/>
<text x="78" y="378" fill="#152214" font-family="Arial,sans-serif" font-size="21" font-weight="700">ENTER MY WEBSITE</text>
<path d="M355 378l15-15m-15 0h15v15" fill="none" stroke="#152214" stroke-width="2.5"/>
<text x="423" y="377" fill="#a6b7c8" font-family="monospace" font-size="14">RESEARCH + COURSES + BILINGUAL AI GUIDES</text>'''
    (assets / 'profile-banner.svg').write_text(svg(hero, 1200, 438, 'Guoliang Wang — MSc student at HKU, working on AI. Enter my website.'))
    cards = [
        ('profile-foundations.svg', '01 / FOUNDATIONS', 'Computer science', '5 courses · 121 explanations', 'Knowledge maps + one-page cheatsheets', '#b8ee91', 'EXPLORE THE COURSES'),
        ('profile-ai.svg', '02 / AI FIELD GUIDES', 'Learn AI through stories', '4 guides · 32 bilingual topics', 'Machine learning, vision + multimodal AI', '#8cdde9', 'CHOOSE A LEARNING PATH'),
    ]
    for filename, label, title, count, detail, color, action in cards:
        body = f'''<path d="M30 29H88" stroke="{color}" stroke-width="3"/>
<text x="30" y="62" fill="{color}" font-family="monospace" font-size="13" letter-spacing="1.5">{label}</text>
<text x="29" y="112" fill="#f2f6fb" font-family="Arial,sans-serif" font-size="29" font-weight="700">{escape(title)}</text>
<text x="30" y="150" fill="#c7d2de" font-family="Arial,sans-serif" font-size="18">{count}</text>
<text x="30" y="180" fill="#91a3b5" font-family="Arial,sans-serif" font-size="15">{escape(detail)}</text>
<path d="M30 207H490" stroke="#293a49"/>
<text x="30" y="243" fill="{color}" font-family="monospace" font-size="14">{action}</text>
<path d="M463 244l16-16m-16 0h16v16" fill="none" stroke="{color}" stroke-width="2"/>'''
        (assets / filename).write_text(svg(body, 520, 275, title + ': ' + count))


def build_profile(root, profile, courses, guides):
    artwork(root)
    username = profile['github'].rstrip('/').rsplit('/', 1)[-1]
    site = f'https://{username}.github.io/{username}/'
    r = profile['research']
    # External page URLs make the same profile links work on GitHub and in previews.
    text = f'''<a href="{site}"><img src="site/assets/profile-banner.svg" width="100%" alt="Guoliang Wang — MSc student at HKU, working on AI. Click to enter my website." /></a>

<p align="center">
  <a href="{site}"><strong>ENTER MY WEBSITE ↗</strong></a> &nbsp; / &nbsp;
  <a href="#about-me">About me</a> &nbsp; / &nbsp;
  <a href="#selected-research">Research</a> &nbsp; / &nbsp;
  <a href="#learning-portals">Courses</a> &nbsp; / &nbsp;
  <a href="mailto:{profile['email']}">Contact</a>
</p>

## About me

{profile['bio']}

| Currently exploring | How I work |
| :--- | :--- |
| Multimodal models and LLM agents | Connect model outputs to verifiable evidence |
| Long-video understanding and generation | Build datasets and evaluate models carefully |
| Efficient video inference | Explain ideas through stories, formulas and examples |

**Tools & interests** · {' · '.join(profile['skills'])}

## Selected research

**[{r['title']}]({r['url']})**

`{r['venue']}` · `{r['role']}` · Long-video understanding

{r['summary']}

{r['contribution']}

[Read the paper ↗]({r['url']}) · [Research on my website ↗]({site}#research)

## Background & experience

'''
    for x in profile['education']:
        text += f'- **{x["institution"]}** · {x["degree"]} · {x["period"]}. {x["detail"]}\n'
    text += '\n'
    for x in profile['experience']:
        text += f'- **{x["role"]}**, {x["organization"]} · {x["period"]}. {x["detail"]}\n'
    text += f'''
**Languages** · {profile['languages']}

## Learning portals

Choose a card to enter the teaching website. Every course connects **story → concept → formula → worked example**.

<table>
<tr>
<td width="50%" align="center"><a href="{site}#learning"><img src="site/assets/profile-foundations.svg" width="100%" alt="Computer science — open five courses, knowledge maps and one-page cheatsheets" /></a><br /><a href="{site}#learning"><strong>Open the course library ↗</strong></a></td>
<td width="50%" align="center"><a href="{site}#ai"><img src="site/assets/profile-ai.svg" width="100%" alt="AI field guides — open four learning paths with English and Chinese versions" /></a><br /><a href="{site}#ai"><strong>Open the bilingual AI guides ↗</strong></a></td>
</tr>
</table>

<details>
<summary><strong>Go straight to a course — all nine learning paths</strong></summary>

### Computer science foundations

| Course | Open the teaching page | Reference |
| :--- | :--- | :--- |
'''
    for c in courses:
        text += f'| {c["code"]} | [{c["title"]}]({site}courses/{c["code"].lower()}.html) | [One-page PDF]({site}downloads/{c["code"]}-cheatsheet.pdf) |\n'
    text += '\n### AI field guides\n\n| Guide | English | Chinese |\n| :--- | :--- | :--- |\n'
    for g in guides:
        text += f'| {g["title"]["en"]} | [Read EN]({site}ai/{g["id"]}.en.html) | [Read ZH]({site}ai/{g["id"]}.zh.html) |\n'
    text += f'''
[Download the complete cheatsheet collection]({site}downloads/guoliang-cheatsheet-collection.pdf)

</details>

<p align="center"><sub>Guoliang · Research, ideas & learning in public.</sub><br /><a href="{site}"><strong>Explore my personal website ↗</strong></a></p>
'''
    (root / 'README.md').write_text(text)
    (root / 'profile' / 'bio.txt').write_text('MSc student @ HKU | Multimodal AI, LLM agents & long-video understanding | AAAI 2026 co-first author\n')
