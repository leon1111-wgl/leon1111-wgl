#!/usr/bin/env python3
"""Rewrite the Projects section of README.md and its small badges from the homepage project list.

The rest of the README is edited by hand. Run after changing PROJECTS in build.py; the order, wording and
demo notes stay in one place so the profile and the website cannot drift apart.
"""
from html import escape as E
from pathlib import Path
import json
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build

ROOT = Path(__file__).resolve().parents[1]
BADGES = ROOT / 'site' / 'assets' / 'badges'


def ink(color):
    """Black or white text, whichever reads better on this project's colour."""
    r, g, b = (int(color[i:i + 2], 16) for i in (1, 3, 5))
    return '#0b0f14' if (0.299 * r + 0.587 * g + 0.114 * b) > 120 else '#ffffff'


def badge(path, text, width, fill, stroke, color):
    path.write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="24" viewBox="0 0 {width} 24" role="img" aria-label="{E(text)}">'
        f'<rect x=".5" y=".5" width="{width - 1}" height="23" rx="5" fill="{fill}" stroke="{stroke}"/>'
        f'<text x="{width / 2}" y="16" text-anchor="middle" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" '
        f'font-size="12" font-weight="600" fill="{color}">{E(text)}</text></svg>\n')


def cell(p, attrs=''):
    pid = p['id']
    demo = f'<a href="{E(p["demo"])}"><img src="site/assets/badges/{pid}-demo.svg" height="24" alt="{E(p["name"])} live demo" /></a>'
    code = f'<a href="https://github.com/leon1111-wgl/{pid}"><img src="site/assets/badges/code.svg" height="24" alt="{E(p["name"])} source code" /></a>'
    return (f'<td{attrs} valign="top">\n<img src="site/assets/icons/{pid}.svg" width="22" height="22" align="absmiddle" alt="" /> '
            f'<b>{E(p["name"])}</b> <sub>{E(p["tag"])}</sub><br />\n{E(p["zh"])}<br />\n<sub>{E(p["en"])}. Try: {E(p["try_en"])}</sub><br /><br />\n'
            f'{demo}&nbsp;{code}\n</td>')


def projects_table():
    first, *rest = build.PROJECTS
    rows = [f'<tr>\n{cell(first, chr(32) + "colspan=" + chr(34) + "2" + chr(34))}\n</tr>']
    for i in range(0, len(rest), 2):
        pair = rest[i:i + 2]
        rows.append('<tr>\n' + '\n'.join(cell(p, ' width="50%"') for p in pair) + '\n</tr>')
    return '<table>\n' + '\n'.join(rows) + '\n</table>'


def main():
    BADGES.mkdir(exist_ok=True)
    for p in build.PROJECTS:
        badge(BADGES / f'{p["id"]}-demo.svg', 'Live demo ↗', 92, p['color'], p['color'], ink(p['color']))
    badge(BADGES / 'code.svg', 'Code', 56, '#111924', '#3a4a5c', '#eaf0f6')
    path = ROOT / 'README.md'
    text = path.read_text()
    new, n = re.subn(r'<!-- projects:start -->.*?<!-- projects:end -->',
                     lambda _: '<!-- projects:start -->\n' + projects_table() + '\n<!-- projects:end -->', text, flags=re.S)
    assert n == 1, 'README.md needs the projects:start and projects:end markers'
    path.write_text(new)
    print(f'README projects: {len(build.PROJECTS)}')


if __name__ == '__main__':
    main()
