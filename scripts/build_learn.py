"""Write the learning hub (site/learn/index.html) from the course, guide and handbook content.

The hub's look and behaviour live in site/learn/learn.css and site/learn/learn.js; this script
only gathers the catalogue (titles, chapters, counts and links) in both languages.
"""
from pathlib import Path
from html import escape as E
import json
import re

from palette import COURSE_COLORS

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'
CONTENT = ROOT / 'content'

# Where each course sits on the suggested route: start → foundations → systems and theory → AI.
TRACKS = {
    'start': {'zh': '入门', 'en': 'Get started'},
    'core': {'zh': '编程基础', 'en': 'Programming foundations'},
    'systems': {'zh': '系统与理论', 'en': 'Systems and theory'},
    'ai': {'zh': '人工智能', 'en': 'Artificial intelligence'},
}
LEVEL = {
    'zero': {'zh': '零基础', 'en': 'Beginner'},
    'intro': {'zh': '入门', 'en': 'Introductory'},
    'core': {'zh': '基础', 'en': 'Foundation'},
    'step': {'zh': '进阶', 'en': 'Intermediate'},
}
ROUTE = [
    ('start', ['python', 'start'],
     {'zh': '先学会运行程序、处理数据，再补上 AI 会用到的数学直觉。',
      'en': 'Learn to run programs and handle data, then pick up the maths intuition that AI uses.'}),
    ('core', ['info1113', 'comp2123'],
     {'zh': '用 Java 理解对象和程序设计，再学算法的正确性和成本。',
      'en': 'Use Java to understand objects and program design, then learn why algorithms are correct and what they cost.'}),
    ('systems', ['comp2017', 'comp2022'],
     {'zh': '看清内存、进程和并发，再理解计算本身的边界。',
      'en': 'See how memory, processes and concurrency work, then where computation itself stops.'}),
    ('ai', ['comp3308', 'ml', 'dl', 'vision', 'multimodal'],
     {'zh': '从搜索与推理，到机器学习、深度学习、计算机视觉和多模态。',
      'en': 'From search and reasoning to machine learning, deep learning, computer vision and multimodal AI.'}),
]

# Where each house stands on the learning map (a 640 × 470 field); the road visits them in ROUTE order.
MAP = {
    'python': (86, 412), 'start': (196, 378), 'info1113': (96, 252), 'comp2123': (186, 150), 'comp2017': (326, 92),
    'comp2022': (452, 118), 'comp3308': (366, 262), 'ml': (478, 290), 'dl': (574, 240), 'vision': (566, 372),
    'multimodal': (440, 402),
}

# Short names for the houses on the hub's learning map.
SHORT = {
    'python': ('Python 入门', 'Python basics'), 'start': ('AI 数学基础', 'AI basics'),
    'info1113': ('Java 面向对象', 'Java OOP'), 'comp2123': ('算法', 'Algorithms'),
    'comp2017': ('C 系统编程', 'C systems'), 'comp2022': ('计算理论', 'Computation'),
    'comp3308': ('人工智能', 'AI'), 'ml': ('机器学习', 'Machine learning'),
    'dl': ('深度学习', 'Deep learning'), 'vision': ('计算机视觉', 'Vision'), 'multimodal': ('多模态', 'Multimodal'),
}

PYTHON_EN = [
    'Start here', 'Programs and basic syntax', 'Variables, types, operators and input',
    'Strings and text processing', 'Comparisons, conditions and branches', 'for loops: one item at a time',
    'while loops and flow control', 'Lists, tuples and object references', 'Dictionaries, sets and nested data',
    'Functions, parameters, return values and scope', 'Comprehensions, sorting and common patterns',
    'Modules, the standard library and environments', 'Paths, files, CSV and JSON',
    'Errors, debugging and validation', 'Classes, objects and methods', 'Reading advanced Python',
    'Python data practice for AI', 'Four complete projects', 'Review route, self-tests and quick reference',
]
PYTHON_STAGES = [
    ({'zh': '跑起第一个程序', 'en': 'Run a first program'}, range(0, 3)),
    ({'zh': '控制程序流程', 'en': 'Control the flow'}, range(3, 7)),
    ({'zh': '组织数据和函数', 'en': 'Organise data and functions'}, range(7, 12)),
    ({'zh': '文件、调试与类', 'en': 'Files, debugging and classes'}, range(12, 16)),
    ({'zh': '面向 AI 的实操与项目', 'en': 'AI practice and projects'}, range(16, 19)),
]


def both(en, zh):
    return {'en': en, 'zh': zh}


def python_handbook():
    page = (SITE / 'python-zero-to-practice' / 'index.html').read_text()
    found = dict(re.findall(r'<article class="chapter" id="(c\d\d)"[^>]*>.*?<h2>([^<]+)</h2>', page))
    found['c00'] = '从这里开始'
    ids = [f'c{i:02d}' for i in range(19)]
    missing = [i for i in ids if i not in found]
    assert not missing, f'Python handbook chapters missing: {missing}'
    chapters = [{'id': i, 'title': both(PYTHON_EN[n], found[i])} for n, i in enumerate(ids)]
    return {
        'id': 'python', 'code': 'INFO1110', 'track': 'start', 'level': 'zero', 'icon': 'python',
        'title': both('Python: Zero to Practice', 'Python 零基础实操'),
        'subtitle': both('From your first print() to small data projects.',
                         '从第一行 print 到独立完成数据处理小项目。'),
        'description': both(
            'For readers who have never programmed. Each unit explains one idea, runs small examples, '
            'and ends with practice that has reference solutions. Short large-model and agent scenes show '
            'where each basic skill is used later. This handbook is in Chinese.',
            '写给完全没学过编程的人。每个单元讲清一个概念，配可运行的小例子，最后是带参考答案的练习。'
            '穿插大模型和 Agent 的小场景，说明这些基础以后用在哪里。'),
        'langs': ['zh'],
        'read': {'zh': 'python-zero-to-practice/index.html'},
        'chapters': chapters,
        'stages': [{'title': t, 'chapters': [ids[i] for i in r]} for t, r in PYTHON_STAGES],
        'stats': {'chapters': 19, 'programs': 105, 'exercises': 114, 'projects': 4},
        'sheet': {'zh': 'python-zero-to-practice/index.html#c18'},
        'notes': {'zh': 'downloads/Python-Zero-to-Practice.zip'},
        'notesKind': 'zip',
        'prerequisites': both(['No programming experience is needed.',
                               'A computer that can install Python 3.10 or newer.'],
                              ['不需要任何编程经验。', '一台能安装 Python 3.10 或更新版本的电脑。']),
        'outcomes': both(['Read and write basic Python programs.', 'Process text, CSV and JSON data.',
                          'Find errors, debug and check results.', 'Finish four complete projects.'],
                         ['读懂并写出基础的 Python 程序。', '处理文本、CSV 和 JSON 数据。',
                          '定位错误、调试并验证结果。', '独立完成 4 个综合项目。']),
    }


def course(code, track, level, icon):
    en = json.loads((CONTENT / f'{code}.json').read_text())
    zh = json.loads((CONTENT / 'translations' / f'{code}.zh.json').read_text())
    assert [t['id'] for t in en['topics']] == [t['id'] for t in zh['topics']], code
    slug = code.lower()
    zt = {t['id']: t for t in zh['topics']}
    return {
        'id': slug, 'code': code, 'track': track, 'level': level, 'icon': icon,
        'title': both(en['title'], zh['title']),
        'subtitle': both(en['subtitle'], zh['subtitle']),
        'description': both(en['description'], zh['description']),
        'langs': ['zh', 'en'],
        'read': {'zh': f'courses/{slug}.zh.html', 'en': f'courses/{slug}.html'},
        'chapters': [{'id': t['id'], 'title': both(t['title'], zt[t['id']]['title'])} for t in en['topics']],
        'stages': [{'title': both(s['title'], z['title']), 'chapters': s['topics']}
                   for s, z in zip(en['map'], zh['map'])],
        'stats': {'chapters': len(en['topics']),
                  'programs': sum(len(t.get('code_examples', [])) for t in en['topics']),
                  'problems': sum(len(t.get('worked_problems', [])) for t in en['topics'])},
        'sheet': {'zh': f'cheatsheets/{slug}.zh.html', 'en': f'cheatsheets/{slug}.html'},
        'pdf': f'downloads/{code}-cheatsheet.pdf',
        'notes': {'zh': f'notes/{code}.zh.md', 'en': f'notes/{code}.md'},
        'notesKind': 'md',
        'prerequisites': both(en['prerequisites'], zh['prerequisites']),
        'outcomes': both(en['outcomes'], zh['outcomes']),
    }


def guide(path, track, level, icon):
    g = json.loads(path.read_text())
    gid = g['id']
    return {
        'id': gid, 'code': g['code'], 'track': track, 'level': level, 'icon': icon,
        'title': g['title'], 'subtitle': g['subtitle'], 'description': g['description'],
        'langs': ['zh', 'en'],
        'read': {'zh': f'ai/{gid}.zh.html', 'en': f'ai/{gid}.en.html'},
        'chapters': [{'id': t['id'], 'title': t['title']} for t in g['topics']],
        'stages': [{'title': s['title'], 'chapters': s['topics']} for s in g['map']],
        'stats': {'chapters': len(g['topics']),
                  'programs': sum(len(t.get('code_examples', [])) for t in g['topics'])},
        'sheet': {'zh': f'ai/{gid}.zh.html#review', 'en': f'ai/{gid}.en.html#review'},
        'notes': {'zh': f'notes/AI-{g["code"]}.zh.md', 'en': f'notes/AI-{g["code"]}.en.md'},
        'notesKind': 'md',
        'prerequisites': g['prerequisites'], 'outcomes': g['outcomes'],
    }


def catalogue():
    paths = CONTENT / 'paths'
    items = [
        python_handbook(),
        guide(CONTENT / 'primer.json', 'start', 'intro', 'start'),
        course('INFO1113', 'core', 'core', 'objects'),
        course('COMP2123', 'core', 'step', 'graph'),
        course('COMP2017', 'systems', 'step', 'chip'),
        course('COMP2022', 'systems', 'step', 'automaton'),
        course('COMP3308', 'ai', 'step', 'search'),
        guide(paths / 'ml.json', 'ai', 'step', 'scatter'),
        guide(paths / 'dl.json', 'ai', 'step', 'layers'),
        guide(paths / 'vision.json', 'ai', 'step', 'eye'),
        guide(paths / 'multimodal.json', 'ai', 'step', 'media'),
    ]
    for c in items:
        c['color'] = COURSE_COLORS[c['id']]
        c['short'] = both(SHORT[c['id']][1], SHORT[c['id']][0])
        assert c['id'] in MAP, f"{c['id']} has no place on the learning map"
        c['map'] = list(MAP[c['id']])
        known = {ch['id'] for ch in c['chapters']}
        for s in c['stages']:
            assert set(s['chapters']) <= known, (c['id'], s['title'])
    ids = {c['id'] for c in items}
    route = [{'track': t, 'courses': cs, 'note': note} for t, cs, note in ROUTE]
    assert all(set(r['courses']) <= ids for r in route)
    totals = {'courses': len(items),
              'chapters': sum(c['stats']['chapters'] for c in items),
              'programs': sum(c['stats'].get('programs', 0) for c in items),
              'sheets': sum(1 for c in items if c.get('pdf'))}
    return {'courses': items, 'route': route, 'tracks': TRACKS, 'levels': LEVEL, 'totals': totals,
            'collection': 'downloads/guoliang-cheatsheet-collection.pdf'}


def version(name):
    from hashlib import sha256
    return sha256((SITE / 'learn' / name).read_bytes()).hexdigest()[:12]


def build():
    data = catalogue()
    links = ''.join(f'<li><a href="../{E(c["read"]["zh"])}">{E(c["code"])} · {E(c["title"]["zh"])}</a></li>'
                    for c in data['courses'])
    payload = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    page = f'''<!doctype html>
<html lang="zh-Hans"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Leon 学习中心 · 中英双语编程与 AI 教程</title>
<meta name="description" content="从零开始的中英双语编程与 AI 教程：Python、Java、C、算法、计算理论和人工智能。每章有故事、原理、公式、例子和可运行代码。">
<meta name="theme-color" content="#000000"><link rel="icon" href="../assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="learn.css?v={version('learn.css')}">
<script id="learn-data" type="application/json">{payload}</script>
<script defer src="learn.js?v={version('learn.js')}"></script>
</head><body><div id="app"><noscript><main class="noscript"><h1>Leon 学习中心</h1><p>请启用 JavaScript 使用课程目录。也可以直接打开：</p><ul>{links}</ul></main></noscript></div></body></html>
'''
    (SITE / 'learn' / 'index.html').write_text(page)
    t = data['totals']
    print(f"learn hub: {t['courses']} courses, {t['chapters']} chapters, {t['programs']} programs")


if __name__ == '__main__':
    build()
