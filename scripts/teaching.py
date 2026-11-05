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
    base = f'examples/{group}/{topic["id"]}-{example["id"]}'
    language = example.get('language', 'python')
    return base + ('/Main.java' if language == 'java' else '.c' if language == 'c' else '.py')


def glossary_html(topic, lang='en'):
    entries = topic.get('glossary', [])
    if not entries:
        return ''
    items = ''.join(f'<div><dt>{E(local(x["term"],lang))}</dt><dd>{E(local(x["meaning"],lang))}</dd></div>' for x in entries)
    return f'<section class="glossary"><h3>{LABELS[lang]["terms"]}</h3><dl>{items}</dl></section>'


DETAIL_LABELS = {
    'en': dict(code='Run a complete example', syntax='Read the syntax', trace='Follow the changing state', problems='Work through a problem', strategy='Choose the method', answer='Interpret the answer', check='Check the reasoning', insights="Leon's further thinking", walk='Follow the execution', download='Download source', command='Run it locally', scroll='Scroll sideways for long lines. Copy or download keeps the original code.'),
    'zh': dict(code='运行一个完整示例', syntax='读懂这里的语法', trace='跟踪状态的变化', problems='完整推导一道题', strategy='先选择方法', answer='解释最终答案', check='检验推理', insights='Leon 的进一步思考', walk='按执行顺序理解', download='下载源代码', command='在本地运行', scroll='长代码行可左右滚动。复制或下载会保留原始代码。')}


def code_html(code, language='python', id=None):
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name
    from pygments.formatters import HtmlFormatter
    rendered = highlight(code.rstrip(), get_lexer_by_name(language, stripnl=False, ensurenl=False), HtmlFormatter(nowrap=True))
    identity = f' id="{E(id)}"' if id else ''
    return f'<pre class="code highlighted" tabindex="0"><code{identity} class="language-{E(language)}">{rendered}</code></pre>'


def command_for(path, language):
    name = Path(path).name
    if language == 'java':
        return 'javac -encoding UTF-8 Main.java\njava -ea Main'
    if language == 'c':
        return f'cc -std=c11 -Wall -Wextra -pedantic -pthread {name} -lm -o demo\n./demo'
    return 'python ' + name


def trace_html(trace, lang):
    if not trace:
        return ''
    head = ''.join('<th scope="col">'+E(local(x,lang))+'</th>' for x in trace['columns'])
    rows = ''.join('<tr>'+''.join('<td>'+E(local(x,lang))+'</td>' for x in row)+'</tr>' for row in trace['rows'])
    return f'<div class="trace-wrap" tabindex="0"><table class="trace-table"><caption>{DETAIL_LABELS[lang]["trace"]}</caption><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>'


def teaching_html(topic, group, lang='en'):
    lab = LABELS[lang]; detail = DETAIL_LABELS[lang]
    pieces = []
    questions = topic.get('guided_questions', [])
    if questions:
        items = ''.join(f'<li><h4>{E(local(x["question"],lang))}</h4>{paragraphs(local(x["answer"],lang))}</li>' for x in questions)
        pieces.append(f'<section class="guided"><h3>{lab["steps"]}</h3><ol>{items}</ol></section>')
    for i, problem in enumerate(topic.get('worked_problems', []), 1):
        steps = ''.join('<li>'+paragraphs(local(x,lang))+'</li>' for x in problem['steps'])
        pieces.append(f'<section class="worked-problem"><h3>{detail["problems"]} · {i:02d}</h3><h4>{E(local(problem["title"],lang))}</h4><div class="problem-question">{paragraphs(local(problem["question"],lang))}</div><h4>{detail["strategy"]}</h4>{paragraphs(local(problem["strategy"],lang))}<ol class="calculation-steps">{steps}</ol><div class="problem-answer"><h4>{detail["answer"]}</h4>{paragraphs(local(problem["answer"],lang))}</div><div class="sanity-check"><h4>{detail["check"]}</h4>{paragraphs(local(problem["sanity_check"],lang))}</div></section>')
    for i, example in enumerate(topic.get('code_examples', []), 1):
        id = f'code-{topic["id"]}-{example["id"]}'
        language = example.get('language','python')
        name = {'python':'Python 3','java':'Java 8+','c':'C11 / POSIX'}[language]
        path = example_path(group,topic,example)
        syntax = ''
        if example.get('syntax_notes'):
            syntax = '<section class="syntax-notes"><h4>'+detail['syntax']+'</h4><dl>'+''.join('<div><dt><code>'+E(x['syntax'])+'</code></dt><dd>'+E(local(x['meaning'],lang))+'</dd></div>' for x in example['syntax_notes'])+'</dl></section>'
        walk = ''
        if example.get('walkthrough'):
            walk = '<h4>'+detail['walk']+'</h4><ol class="execution-steps">'+''.join('<li>'+paragraphs(local(x,lang))+'</li>' for x in example['walkthrough'])+'</ol>'
        pieces.append(f'''<section class="code-example" id="lab-{topic["id"]}-{example["id"]}" data-reading-id="lab-{topic["id"]}-{example["id"]}"><h3>{detail['code']} · {i:02d}</h3><h4>{E(local(example['title'],lang))}</h4>{paragraphs(local(example['intro'],lang))}<div class="code-actions"><span>{name}</span><button type="button" data-copy-code="{id}">{lab['copy']}</button><a href="../{path}" download>{detail['download']} ↓</a><p class="code-hint">{detail['scroll']}</p></div>{code_html(example['code'],language,id)}<details class="example-run"><summary>{detail['command']}</summary><pre class="code">{E(command_for(path,language))}</pre></details><div class="output-block"><h4>{lab['output']}</h4><pre class="code code-output">{E(example['output'])}</pre></div>{syntax}{walk}{trace_html(example.get('trace'),lang)}<h4>{lab['explain']}</h4>{paragraphs(local(example['explanation'],lang))}</section>''')
    cases = topic.get('practice_cases', [])
    if cases:
        items = ''.join(f'<article><h4>{E(local(x["title"],lang))}</h4>{paragraphs(local(x["body"],lang))}</article>' for x in cases)
        pieces.append(f'<section class="practice-cases"><h3>{lab["cases"]}</h3>{items}</section>')
    if topic.get('instructor_notes'):
        notes = ''.join('<article><h4>'+E(local(x['title'],lang))+'</h4>'+paragraphs(local(x['body'],lang))+'</article>' for x in topic['instructor_notes'])
        pieces.append('<section class="instructor-notes"><h3>'+detail['insights']+'</h3>'+notes+'</section>')
    return ''.join(pieces)


def teaching_markdown(topic, group, lang='en'):
    lab = LABELS[lang]; detail = DETAIL_LABELS[lang]
    parts = []
    if topic.get('glossary'):
        parts.append('### ' + lab['terms'])
        parts.extend(f'- **{local(x["term"],lang)}:** {local(x["meaning"],lang)}' for x in topic['glossary'])
    if topic.get('guided_questions'):
        parts.append('### ' + lab['steps'])
        for x in topic['guided_questions']:
            parts.extend(['**' + local(x['question'],lang) + '**', local(x['answer'],lang)])
    for problem in topic.get('worked_problems', []):
        parts.extend(['### '+local(problem['title'],lang), local(problem['question'],lang), '**'+detail['strategy']+'**',local(problem['strategy'],lang)])
        parts.extend(f'{i}. {local(x,lang)}' for i,x in enumerate(problem['steps'],1))
        parts.extend(['**'+detail['answer']+'**',local(problem['answer'],lang),'**'+detail['check']+'**',local(problem['sanity_check'],lang)])
    for example in topic.get('code_examples', []):
        language = example.get('language','python')
        parts.extend([f'<a id="lab-{topic["id"]}-{example["id"]}"></a>', '### '+local(example['title'],lang), local(example['intro'],lang), '```'+language+'\n'+example['code'].rstrip()+'\n```', '**'+detail['command']+'**', '```sh\n'+command_for(example_path(group,topic,example),language)+'\n```', '**'+lab['output']+'**', '```text\n'+example['output'].rstrip()+'\n```'])
        if example.get('syntax_notes'):
            parts.append('**'+detail['syntax']+'**')
            parts.extend('- `'+x['syntax']+'`: '+local(x['meaning'],lang) for x in example['syntax_notes'])
        if example.get('walkthrough'):
            parts.append('**'+detail['walk']+'**')
            parts.extend(f'{i}. {local(x,lang)}' for i,x in enumerate(example['walkthrough'],1))
        if example.get('trace'):
            trace=example['trace']; cell=lambda x: local(x,lang).replace('|','\\|').replace('\n','<br>')
            table=['| '+' | '.join(cell(x) for x in trace['columns'])+' |','| '+' | '.join('---' for _ in trace['columns'])+' |']
            table.extend('| '+' | '.join(cell(x) for x in row)+' |' for row in trace['rows'])
            parts.extend(['**'+detail['trace']+'**','\n'.join(table)])
        parts.extend(['**'+lab['explain']+'**',local(example['explanation'],lang)])
    if topic.get('practice_cases'):
        parts.append('### '+lab['cases'])
        for x in topic['practice_cases']:parts.extend(['**'+local(x['title'],lang)+'**',local(x['body'],lang)])
    if topic.get('instructor_notes'):
        parts.append('### '+detail['insights'])
        for x in topic['instructor_notes']:parts.extend(['**'+local(x['title'],lang)+'**',local(x['body'],lang)])
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
                language = example.get('language','python')
                prefix = '#' if language == 'python' else '//'
                header = f'{prefix} Leon | Original learning example\n{prefix} '+local(example['title'],'en')+'\n'
                if language=='python':
                    header += '# Python 3.12+ | Run: python '+path.name+'\n'
                    if 'numpy' in example['code']:header += '# Install once with the same Python: python -m pip install numpy\n'
                path.write_text(header+example['code'].rstrip()+'\n')
                manifest.append({'path':relative,'language':language,'group':group,'topic':topic['id'],'title':local(example['title'],'en'),'output':example['output'],'run':command_for(relative,language)})
    folder = ROOT/'site'/'examples'
    folder.mkdir(exist_ok=True)
    manifest_text=json.dumps(manifest,indent=2,ensure_ascii=False)+'\n'
    (folder/'manifest.json').write_text(manifest_text)
    readme = '# Leon code examples\n\nEach example has a complete program, expected output and a step-by-step explanation on its topic page. These small examples explain mechanisms; they are not complete production systems.\n\n## Python\n\nUse Python 3.12+. Run `python filename.py`. If the file imports NumPy, first run `python -m pip install numpy` using the same Python. No model or dataset downloads are needed.\n\n## Java\n\nUse JDK 8 or newer. Open one example folder, then run `javac -encoding UTF-8 Main.java` and `java -ea Main`. Each folder is an independent program; do not compile all Main.java files together.\n\n## C\n\nUse a C11 compiler on macOS or a POSIX system such as Linux. Open an example folder and compile the chosen file with `cc -std=c11 -Wall -Wextra -pedantic -pthread filename.c -lm -o demo`, then run `./demo`. Windows needs a POSIX environment such as WSL for the process and thread examples. Programs create only temporary/local demo data.\n\n## Index\n\n' + '\n'.join(f'- [{x["group"]}: {x["title"]}]({x["path"].removeprefix("examples/")})' for x in manifest)+'\n'
    (folder/'README.md').write_text(readme)
    for filename, entries in [('guoliang-code-examples.zip',manifest),('guoliang-python-examples.zip',[x for x in manifest if x['language']=='python'])]:
        destination=ROOT/'site'/'downloads'/filename
        with ZipFile(destination,'w',ZIP_DEFLATED) as z:
            archive_readme=readme.split('## Index\n\n')[0]+'## Index\n\n'+'\n'.join(f'- [{x["group"]}: {x["title"]}]({x["path"].removeprefix("examples/")})' for x in entries)+'\n'
            files={'examples/README.md':archive_readme.encode(),'examples/manifest.json':(json.dumps(entries,indent=2,ensure_ascii=False)+'\n').encode()}
            files.update({x['path']:(ROOT/'site'/x['path']).read_bytes() for x in entries})
            for name,data in files.items():
                info=ZipInfo(name,date_time=(2026,1,1,0,0,0));info.compress_type=ZIP_DEFLATED;info.external_attr=0o100644 << 16
                z.writestr(info,data)
    return manifest


def course_reading_tools(code, lang='en'):
    if code not in ('COMP2017','INFO1113'):
        return reading_tools(lang)
    zh=lang=='zh'
    lab=LABELS[lang]
    language='Java' if code=='INFO1113' else 'C'
    if language=='Java':
        helptext=('JDK 是 Java Development Kit，即 Java 开发工具包。使用 JDK 8 或更新版本。它包含 javac 编译器和 java 启动命令。JVM 是 Java 虚拟机，负责执行编译后的字节码。\n\n每个可下载示例都是独立的 Main.java。将它保存在单独文件夹中，保持文件名为 Main.java。在这个文件夹中打开终端，再输入下方两行命令。终端是输入命令、查看文字结果的窗口。\n\njavac 把源代码编译成 .class 文件；java 启动程序。-encoding UTF-8 指定源文件编码；-ea 启用 assert 检查。把结果与页面的预期输出比较。'
                  if zh else
                  'JDK means Java Development Kit. Use JDK 8 or newer. It includes the javac compiler and the java launcher. JVM means Java Virtual Machine. It runs the compiled bytecode.\n\nEach downloadable example is a separate Main.java program. Save it in its own folder and keep that exact file name. Open a terminal in that folder, then enter the two lines below. A terminal is a window for typing commands and reading text results.\n\njavac compiles the source into .class files. java starts the program. -encoding UTF-8 sets the source encoding; -ea enables assert checks. Compare the result with the expected output on the page.')
        commands='javac -encoding UTF-8 Main.java\njava -ea Main'
        reference='<a href="https://dev.java/learn/first-steps/">'+('Java 官方入门与安装指引' if zh else 'Official Java setup and first steps')+' ↗</a>'
    else:
        helptext=('编译器把 C 源代码转换成可执行程序。使用 macOS 或 Linux 上的 C11 编译器。进程、信号和线程示例需要 POSIX 系统接口；Windows 可使用 WSL 中的 Linux 环境。\n\n下载一个示例，在它所在的文件夹中打开终端。终端是输入命令、查看文字结果的窗口。把 filename.c 换成实际文件名。先编译，再运行 ./demo：./ 表示当前文件夹，demo 是生成的程序。\n\n-std=c11 选择 C11；-Wall、-Wextra 和 -pedantic 打开更多诊断；-pthread 启用线程支持；-lm 链接数学库；-o demo 指定输出程序名称。结果应与页面的预期输出一致。'
                  if zh else
                  'A compiler turns C source text into an executable program. Use a C11 compiler on macOS or Linux. Process, signal and thread examples need POSIX system interfaces. On Windows, use a Linux environment such as WSL.\n\nDownload one example and open a terminal in its folder. A terminal is a window for commands and text results. Replace filename.c with the actual name. Compile first, then run ./demo. The ./ means the current folder; demo is the program you built.\n\n-std=c11 selects C11. -Wall, -Wextra and -pedantic enable more diagnostics. -pthread enables thread support; -lm links the maths library; -o demo names the output program. Compare its result with the expected output.')
        commands='cc -std=c11 -Wall -Wextra -pedantic -pthread filename.c -lm -o demo\n./demo'
        reference='<a href="https://clang.llvm.org/get_started.html">'+('Clang 官方编译器说明' if zh else 'Official Clang compiler guide')+' ↗</a>'
    title='第一次运行这些示例？' if zh else 'Running these examples for the first time?'
    download='下载全部 Python、Java 和 C 示例' if zh else 'Download all Python, Java and C examples'
    return f'<div class="reading-tools"><div role="group" aria-label="{lab["size"]}"><span>{lab["size"]}</span><button type="button" data-reading-size="normal" aria-pressed="true">A · {lab["normal"]}</button><button type="button" data-reading-size="large" aria-pressed="false">A+ · {lab["large"]}</button></div><a href="../downloads/guoliang-code-examples.zip" download>{download} ↓</a><details class="run-help"><summary>{title}</summary>{paragraphs(helptext)}<pre class="code">{E(commands)}</pre><p>{reference}</p></details></div>'
