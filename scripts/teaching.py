"""Render and export the teaching blocks shared by courses and AI guides."""
from pathlib import Path
from html import escape as E

ROOT = Path(__file__).resolve().parents[1]
LABELS = {
    'en': {'terms': 'Words to know', 'steps': 'Let us work through it', 'code': 'Try the idea in Python', 'output': 'Expected output', 'explain': 'Read the code step by step', 'download': 'Download Python', 'copy': 'Copy code', 'cases': 'Where you can use this', 'size': 'Text size', 'normal': 'Comfortable', 'large': 'Larger', 'primer': 'New to Python or the maths? Start here', 'allcode': 'Download all Python examples'},
    'zh': {'terms': '先认识这些词', 'steps': '一步步想清楚', 'code': '用 Python 跑一遍', 'output': '预期输出', 'explain': '逐步读懂代码', 'download': '下载 Python 代码', 'copy': '复制代码', 'cases': '这些知识可以用在哪里', 'size': '阅读字号', 'normal': '舒适', 'large': '更大', 'primer': '刚接触 Python 或这些数学知识？从这里开始', 'allcode': '下载全部 Python 示例'},
}
LEVELS = {'foundation': {'en': 'Foundation', 'zh': '入门'}, 'core': {'en': 'Core idea', 'zh': '核心'}, 'applied': {'en': 'In practice', 'zh': '应用'}, 'advanced': {'en': 'Going deeper', 'zh': '进阶'}}


def local(value, lang):
    return value[lang] if isinstance(value, dict) else value


def paragraphs(value):
    return ''.join('<p>' + E(p).replace('\n', '<br>') + '</p>' for p in value.split('\n\n') if p)


def example_path(group, topic, example):
    return f'examples/{group}/{topic["id"]}-{example["id"]}.py'


def glossary_html(topic, lang='en'):
    entries = topic.get('glossary', [])
    if not entries:
        return ''
    items = ''.join(f'<div><dt>{E(local(x["term"],lang))}</dt><dd>{E(local(x["meaning"],lang))}</dd></div>' for x in entries)
    return f'<section class="glossary"><h3>{LABELS[lang]["terms"]}</h3><dl>{items}</dl></section>'


def teaching_html(topic, group, lang='en'):
    lab = LABELS[lang]
    pieces = []
    questions = topic.get('guided_questions', [])
    if questions:
        items = ''.join(f'<li><h4>{E(local(x["question"],lang))}</h4>{paragraphs(local(x["answer"],lang))}</li>' for x in questions)
        pieces.append(f'<section class="guided"><h3>{lab["steps"]}</h3><ol>{items}</ol></section>')
    for example in topic.get('code_examples', []):
        id = f'code-{topic["id"]}-{example["id"]}'
        pieces.append(f'''<section class="code-example"><h3>{lab['code']}</h3><h4>{E(local(example['title'],lang))}</h4>{paragraphs(local(example['intro'],lang))}<div class="code-actions"><span>Python 3</span><button type="button" data-copy-code="{id}">{lab['copy']}</button><a href="../{example_path(group,topic,example)}" download>{lab['download']} ↓</a></div><pre class="code"><code id="{id}" class="language-python">{E(example['code'])}</code></pre><h4>{lab['output']}</h4><pre class="code code-output">{E(example['output'])}</pre><h4>{lab['explain']}</h4>{paragraphs(local(example['explanation'],lang))}</section>''')
    cases = topic.get('practice_cases', [])
    if cases:
        items = ''.join(f'<article><h4>{E(local(x["title"],lang))}</h4>{paragraphs(local(x["body"],lang))}</article>' for x in cases)
        pieces.append(f'<section class="practice-cases"><h3>{lab["cases"]}</h3>{items}</section>')
    return ''.join(pieces)


def teaching_markdown(topic, group, lang='en'):
    lab = LABELS[lang]
    parts = []
    if topic.get('glossary'):
        parts.append('### ' + lab['terms'])
        parts.extend(f'- **{local(x["term"],lang)}:** {local(x["meaning"],lang)}' for x in topic['glossary'])
    if topic.get('guided_questions'):
        parts.append('### ' + lab['steps'])
        for x in topic['guided_questions']:
            parts.extend(['**' + local(x['question'],lang) + '**', local(x['answer'],lang)])
    for example in topic.get('code_examples', []):
        parts.extend(['### '+local(example['title'],lang), local(example['intro'],lang), '```python\n'+example['code'].rstrip()+'\n```', '**'+lab['output']+'**', '```text\n'+example['output'].rstrip()+'\n```', '**'+lab['explain']+'**', local(example['explanation'],lang)])
    if topic.get('practice_cases'):
        parts.append('### '+lab['cases'])
        for x in topic['practice_cases']:
            parts.extend(['**'+local(x['title'],lang)+'**',local(x['body'],lang)])
    return '\n\n'.join(parts)


def asset_version(filename):
    from hashlib import sha256
    return sha256((ROOT/'site'/'assets'/filename).read_bytes()).hexdigest()[:12]


def run_notes(lang='en'):
    if lang == 'zh':
        return '### 运行 Python 示例\n\n使用 Python 3.12 或更新版本。把代码保存为 .py 文件，在终端中用 `python 文件名.py` 运行；部分系统使用 `python3`。若出现 `import numpy as np`，先运行 `python -m pip install numpy`。这行 import 加载 NumPy 数值工具包，并把它简称为 np。示例无需下载数据集或模型权重。\n\n[Python 官方下载](https://www.python.org/downloads/) · [NumPy 官方安装说明](https://numpy.org/install/)'
    return '### Run the Python examples\n\nUse Python 3.12 or newer. Save the code as a .py file. In a terminal, run `python filename.py`; some systems use `python3`. If the code contains `import numpy as np`, first run `python -m pip install numpy`. The import loads NumPy, a package for numeric arrays, and gives it the short name np. No dataset or model-weight downloads are needed.\n\n[Official Python downloads](https://www.python.org/downloads/) · [Official NumPy installation guide](https://numpy.org/install/)'


def run_help(lang):
    if lang == 'zh':
        return '''<details class="run-help"><summary>第一次运行 Python？按这四步操作</summary><ol><li>安装 Python 3.12 或更新版本。<a href="https://www.python.org/downloads/">Python 官方下载页 ↗</a></li><li>点击示例旁的“下载 Python 代码”，得到一个 .py 文件。它是包含程序文字的文件。</li><li>打开终端，在下载目录中运行 <code>python 文件名.py</code>，并把“文件名”换成实际名称。在部分系统上，命令是 <code>python3</code>。终端是输入命令并查看文字结果的窗口。</li><li>把运行结果与页面的“预期输出”逐项比较。先改一个输入，再观察变化。</li></ol><p>部分示例使用 NumPy，这是处理数字和数组的工具包。若代码中出现 <code>import numpy as np</code>，请先用同一 Python 安装一次：<code>python -m pip install numpy</code>。这行 import 加载 NumPy，并把它简称为 np。<a href="https://numpy.org/install/">NumPy 官方安装说明 ↗</a></p><p>示例无需下载数据集或模型权重。安装 Python 和所需工具包后即可离线运行。页面上的代码文字可以复制；运行结果会显示在你的终端中。</p></details>'''
    return '''<details class="run-help"><summary>Running Python for the first time? Follow four steps</summary><ol><li>Install Python 3.12 or newer. <a href="https://www.python.org/downloads/">Official Python downloads ↗</a></li><li>Choose “Download Python” beside an example. The .py file contains the program as text.</li><li>Open a terminal in the download folder. Run <code>python filename.py</code>, using the actual file name. Some systems use <code>python3</code> instead. A terminal is a window where you type commands and read text results.</li><li>Compare each result with “Expected output” on this page. Change one input and observe the difference.</li></ol><p>Some examples use NumPy, a package for numbers and arrays. If the code contains <code>import numpy as np</code>, install NumPy once with the same Python: <code>python -m pip install numpy</code>. The import line loads NumPy and gives it the short name np. <a href="https://numpy.org/install/">Official NumPy installation guide ↗</a></p><p>No dataset or model-weight downloads are needed. Examples run offline after Python and any required package are installed. You can copy the code from the page; its output appears in your terminal.</p></details>'''


def reading_tools(lang='en', show_primer=True):
    lab = LABELS[lang]
    primer_link = f'<a href="../ai/start.{lang}.html">{lab["primer"]} ↗</a>' if show_primer else ''
    return f'''<div class="reading-tools"><div role="group" aria-label="{lab['size']}"><span>{lab['size']}</span><button type="button" data-reading-size="normal" aria-pressed="true">A · {lab['normal']}</button><button type="button" data-reading-size="large" aria-pressed="false">A+ · {lab['large']}</button></div>{primer_link}<a href="../downloads/guoliang-python-examples.zip" download>{lab['allcode']} ↓</a>{run_help(lang)}</div>'''


def export_examples(documents):
    import json
    from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED
    manifest = []
    for group, document in documents:
        for topic in document['topics']:
            for example in topic.get('code_examples', []):
                relative = example_path(group,topic,example)
                path = ROOT/'site'/relative
                path.parent.mkdir(parents=True,exist_ok=True)
                header = '# Guoliang | Original learning example\n# '+local(example['title'],'en')+'\n# Python 3.12+ | Run: python '+path.name+'\n'
                if 'numpy' in example['code']:
                    header += '# Install once with the same Python: python -m pip install numpy\n'
                path.write_text(header+example['code'].rstrip()+'\n')
                manifest.append({'path':relative,'group':group,'topic':topic['id'],'title':local(example['title'],'en'),'output':example['output']})
    folder = ROOT/'site'/'examples'
    folder.mkdir(exist_ok=True)
    (folder/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
    (folder/'README.md').write_text('# Guoliang Python examples\n\nUse Python 3.12 or newer. Most examples use only the standard library. Examples that import NumPy need `python -m pip install numpy`. No data downloads or trained model weights are needed.\n\nRun a file with `python path/to/example.py`. Its topic page explains the input, expected output and limitations. These small examples explain mechanisms. They are not complete production systems.\n\n'+ '\n'.join(f'- [{x["group"]}: {x["title"]}]({x["path"].removeprefix("examples/")})' for x in manifest)+'\n')
    destination = ROOT/'site'/'downloads'/'guoliang-python-examples.zip'
    with ZipFile(destination,'w',ZIP_DEFLATED) as z:
        for path in [folder/'README.md',folder/'manifest.json']+[ROOT/'site'/x['path'] for x in manifest]:
            info = ZipInfo(str(path.relative_to(ROOT/'site')), date_time=(2026,1,1,0,0,0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info,path.read_bytes())
    return manifest
