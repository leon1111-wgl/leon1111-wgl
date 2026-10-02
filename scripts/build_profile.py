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


def artwork(root, courses, guides):
    assets = root / 'site' / 'assets'
    hero = '''<ellipse cx="705" cy="150" rx="230" ry="200" fill="url(#glow)"/>
<path d="M36 37H804" stroke="#2a3b4b"/>
<g fill="#b8ee91"><circle cx="42" cy="36" r="5"/><circle cx="62" cy="36" r="5" opacity=".6"/><circle cx="82" cy="36" r="5" opacity=".3"/></g>
<text x="32" y="123" fill="#f2f6fb" font-family="Arial,sans-serif" font-size="64" font-weight="700" letter-spacing="-2">Guoliang Wang</text>
<text x="36" y="179" fill="#b8ee91" font-family="Arial,sans-serif" font-size="34">MSc @ HKU · AI</text>
<g fill="none" stroke="#527e86"><circle cx="665" cy="159" r="86"/><circle cx="665" cy="159" r="61" stroke-dasharray="3 9"/><ellipse cx="665" cy="159" rx="122" ry="45" transform="rotate(-35 665 159)"/><path d="M611 89L751 181L606 219L611 89M751 181L665 159L611 89"/></g>
<g fill="#b8ee91"><circle cx="611" cy="89" r="5"/><circle cx="751" cy="181" r="5"/><circle cx="606" cy="219" r="5"/></g>
<circle cx="665" cy="159" r="35" fill="#101d29" stroke="#b8ee91"/>
<text x="665" y="170" text-anchor="middle" fill="#f2f6fb" font-family="monospace" font-size="31">GW</text>
<rect x="36" y="222" width="365" height="62" rx="9" fill="#b8ee91"/>
<text x="58" y="263" fill="#152214" font-family="Arial,sans-serif" font-size="32" font-weight="700">Explore my site</text>
<path d="M346 263l19-19m-19 0h19v19" fill="none" stroke="#152214" stroke-width="3"/>'''
    (assets / 'profile-banner.svg').write_text(svg(hero,840,320,'Guoliang Wang — MSc student at HKU, working on AI. Enter my website.'))
    for filename,title,code,color in [('profile-foundations.svg','Foundations','CS','#b8ee91'),('profile-ai.svg','AI guides','AI','#8cdde9')]:
        body=f'''<path d="M30 30H110" stroke="{color}" stroke-width="4"/>
<text x="30" y="95" fill="#f2f6fb" font-family="Arial,sans-serif" font-size="50" font-weight="700">{title}</text>
<text x="30" y="168" fill="{color}" font-family="monospace" font-size="36">{code}</text>
<circle cx="444" cy="159" r="30" fill="none" stroke="{color}"/>
<path d="M432 171l24-24m-24 0h24v24" fill="none" stroke="{color}" stroke-width="3"/>'''
        (assets / filename).write_text(svg(body,520,210,title))


def build_profile(root, profile, courses, guides):
    artwork(root, courses, guides)
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

Choose a card to enter the teaching website. Follow **story → concept → formula → worked example**. AI guides and data structures include runnable Python, expected outputs and step-by-step explanations.

**New to Python or AI?** [Start here in English]({site}ai/start.en.html) · [Start here in Chinese]({site}ai/start.zh.html) · [Download Python examples]({site}downloads/guoliang-python-examples.zip)

<table>
<tr>
<td width="50%" align="center"><a href="{site}#learning"><img src="site/assets/profile-foundations.svg" width="100%" alt="Computer science — open five courses, knowledge maps and one-page cheatsheets" /></a><br /><a href="{site}#learning"><strong>Open the course library ↗</strong></a><p>{len(courses)} courses · {sum(len(c["topics"]) for c in courses)} topics</p></td>
<td width="50%" align="center"><a href="{site}#ai"><img src="site/assets/profile-ai.svg" width="100%" alt="AI field guides — open four learning paths with English and Chinese versions" /></a><br /><a href="{site}#ai"><strong>Open the bilingual AI guides ↗</strong></a><p>{len(guides)} guides · {sum(len(g["topics"]) for g in guides)} bilingual topics</p></td>
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
