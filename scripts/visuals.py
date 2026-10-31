"""Interactive step-through diagrams placed after a chapter's worked example (drawn by site/assets/viz.js)."""
from html import escape as E
from pathlib import Path
import json

VISUALS = json.loads((Path(__file__).resolve().parents[1] / 'content' / 'visuals.json').read_text())
KICKER = {'en': 'See it run', 'zh': '动手看一看'}
HINT = {'en': 'Press play, or step through with the arrows.', 'zh': '点播放自动演示，或者用箭头一步一步看。'}
NOSCRIPT = {'en': 'This diagram needs JavaScript. The worked example above covers the same steps.',
            'zh': '这个图示需要启用 JavaScript。上面的例子讲的是同样的步骤。'}


def visual_html(code, topic_id, lang):
    v = VISUALS.get(code, {}).get(topic_id)
    if not v:
        return ''
    return (f'<figure class="viz" data-viz="{v["kind"]}"><figcaption><span class="viz-kicker">{KICKER[lang]}</span>'
            f'<b>{E(v["title"][lang])}</b><span class="viz-hint">{HINT[lang]}</span></figcaption>'
            f'<div class="viz-body"></div><noscript><p>{NOSCRIPT[lang]}</p></noscript></figure>')
