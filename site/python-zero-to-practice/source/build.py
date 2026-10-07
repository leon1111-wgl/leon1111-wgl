"""生成离线教材与练习文件；仅使用标准库。重建不会覆盖已存在的练习文件。"""
from pathlib import Path
import html, re, json, io, tokenize, keyword
from course_data import CHAPTERS
from project_data import PROJECTS
from starter_templates import STARTERS
ROOT = Path(__file__).resolve().parent.parent
ESC = html.escape

def write(path, text, preserve=False):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    if not (preserve and target.exists()):
        target.write_text(text, encoding='utf-8')

def inline(text):
    saved = []
    def code(match):
        saved.append('<code>'+ESC(match.group(1))+'</code>')
        return f'\x00{len(saved)-1}\x00'
    text = re.sub(r'`([^`]+)`', code, text)
    text = ESC(text)
    text = re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)', r'<a href="\2" target="_blank" rel="noreferrer">\1</a>', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\x00(\d+)\x00', lambda m:saved[int(m[1])], text)
    return text

def highlight(code):
    lines=code.splitlines(keepends=True)
    offsets=[0]
    for line in lines: offsets.append(offsets[-1]+len(line))
    def pos(p): return offsets[min(p[0]-1,len(offsets)-1)]+p[1]
    output=[]; last=0
    try:
        for token in tokenize.generate_tokens(io.StringIO(code).readline):
            if token.type in (tokenize.ENDMARKER, tokenize.ENCODING): continue
            a,b=pos(token.start),pos(token.end)
            if b<=a or a<last: continue
            output.append(ESC(code[last:a]))
            kind = 'str' if token.type==tokenize.STRING else 'comment' if token.type==tokenize.COMMENT else 'num' if token.type==tokenize.NUMBER else 'kw' if token.type==tokenize.NAME and keyword.iskeyword(token.string) else ''
            output.append(f'<span class="tok-{kind}">{ESC(code[a:b])}</span>' if kind else ESC(code[a:b]))
            last=b
        output.append(ESC(code[last:]))
        return ''.join(output)
    except (tokenize.TokenError, IndentationError): return ESC(code)

def codeblock(code, label='Python', copy=True):
    formatted = highlight(code) if label=='Python' else ESC(code)
    button = '<button class="copy" type="button">复制代码</button>' if copy else ''
    return f'<div class="codebox"><div class="codebar"><span>{ESC(label)}</span>{button}</div><pre><code>{formatted.rstrip()}</code></pre></div>'

def md(text, prefix=''):
    lines=text.splitlines(); out=[]; i=0; part=0
    while i<len(lines):
        line=lines[i]
        if not line.strip(): i+=1; continue
        if line.startswith('```'):
            lang=line[3:]; block=[]; i+=1
            while i<len(lines) and not lines[i].startswith('```'):
                block.append(lines[i]); i+=1
            out.append(codeblock('\n'.join(block), '终端命令' if lang=='terminal' else 'Python')); i+=1; continue
        if line.startswith('### '):
            part+=1; out.append(f'<h3 id="{prefix}-part{part}">{inline(line[4:])}</h3>'); i+=1; continue
        if line.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].startswith('|'):
                rows.append([cell.strip() for cell in lines[i].strip().strip('|').split('|')]); i+=1
            out.append('<div class="table-wrap"><table><thead><tr>'+''.join('<th>'+inline(x)+'</th>' for x in rows[0])+'</tr></thead><tbody>')
            for row in rows[2:]: out.append('<tr>'+''.join('<td>'+inline(x)+'</td>' for x in row)+'</tr>')
            out.append('</tbody></table></div>'); continue
        if re.match(r'^(- |\d+\. )',line):
            ordered=not line.startswith('- '); tag='ol' if ordered else 'ul'; out.append('<'+tag+'>')
            while i<len(lines) and re.match(r'^(- |\d+\. )',lines[i]):
                out.append('<li>'+inline(re.sub(r'^(- |\d+\. )','',lines[i]))+'</li>'); i+=1
            out.append('</'+tag+'>'); continue
        block=[line]; i+=1
        while i<len(lines) and lines[i].strip() and not re.match(r'^(### |```|\||- |\d+\. )',lines[i]):
            block.append(lines[i]); i+=1
        out.append('<p>'+inline('\n'.join(block))+'</p>')
    return '\n'.join(out)

EXAMPLES=[]; EXERCISES=[]
for c in CHAPTERS:
    n=c['number']
    for e in c['examples']:
        path=f'examples/ch{n:02d}/ex{e["id"]}.py'; e['path']=path
        write(path, '# '+e['title']+'\n'+e['code']); EXAMPLES.append(e)
    for e in c['exercises']:
        e['path']=f'practice/ch{n:02d}/ex{e["id"]}.py'
        solution=f'solutions/ch{n:02d}/ex{e["id"]}.py'; e['solution']=solution
        header = '# 第 '+e['id']+' 题 '+e['title']+'\n# '+e['task']+'\n# 预期程序输出：\n'+''.join('# '+line+'\n' for line in e['output'].splitlines())
        if e['stdin']: header+='# 自检时提供输入：'+repr(e['stdin'])+'\n'
        write(e['path'],header+'\n# 请在下面独立作答。先保存，再运行。\n',preserve=True)
        write(solution,header+'\n'+e['code']); EXERCISES.append(e)
write('tools/manifest.json',json.dumps({'examples':EXAMPLES,'exercises':EXERCISES},ensure_ascii=False,indent=2))

project_html=[]; project_text=[]
for p in PROJECTS:
    folder='projects/'+p['folder']
    write(folder+'/app.py',p['code'])
    for path,data in p['data'].items(): write(folder+'/'+path,data)
    steps='\n\n'.join(f'### {i+1} {title}\n{body}' for i,(title,body) in enumerate(p['steps']))
    text=f'# {p["title"]}\n\n前置：{p["prerequisites"]}\n\n{p["task"]}\n\n{steps}\n\n### 运行命令\n\n从学习包根目录执行。Windows 用 py，Mac 用 python3，激活环境后可用 python。\n\n```terminal\n{p["commands"]}\n```\n\n### 预期结果\n\n{p["expected"]}\n\n### 验收\n\n运行学习包的 python tools/check_projects.py 核验参考实现；自己的实现按上面手算结果和边界逐项验证。\n'
    write(folder+'/README.md',text)
    write(folder+'/TASKS.md',text+'\n\n## 独立实现记录\n\n- 输入约定：\n- 输出约定：\n- 最小样例手算：\n- 空数据测试：\n- 边界测试：\n- 错误输入测试：\n- 我的新增功能：\n')
    write(folder+'/starter.py',STARTERS[p['folder']],preserve=True)
    block=f'<section class="project" id="c17-{p["folder"]}"><div class="eyebrow">PROJECT {p["folder"][:2]}</div><h3>{ESC(p["title"])}</h3><p class="muted">前置：{ESC(p["prerequisites"])}</p><p>{ESC(p["task"])}</p>{md(steps,"p"+p["folder"])}<h4>运行命令</h4>{codeblock(p["commands"],"终端命令")}<h4>预期结果与输出位置</h4><p>{ESC(p["expected"])}</p><p><a download href="{folder}/TASKS.md">保存项目任务书</a> · <a download href="{folder}/app.py">保存完整参考代码</a></p><details><summary>展开完整实现（建议先尝试）</summary>{codeblock(p["code"])}<p>逐步对照任务书，确认每个函数在处理哪一层数据。</p></details></section>'
    project_html.append(block); project_text.append(text+'\n\n```python\n'+p['code']+'```\n')
write('tools/project_checks.json',json.dumps([{k:p[k] for k in ['folder','checks']} for p in PROJECTS],ensure_ascii=False,indent=2))

SIMS={
5: '<section class="lab" data-lab="loop"><div class="eyebrow">动手看执行过程</div><h3>每轮 total 怎样变化</h3><p>固定程序：对 [2, 4, 1] 执行 total += value。先预测下一轮 total，再点下一步。</p><div class="lab-screen" aria-live="polite"></div><div class="lab-actions"><button data-step="-1">上一步</button><button data-step="1">下一步</button><button data-reset>重新开始</button></div><p class="muted">这是预设步骤演示；真实 Python 请运行示例 05_02。</p></section>',
7: '<section class="lab" data-lab="alias"><div class="eyebrow">动手看对象关系</div><h3>赋值与浅拷贝为什么不同</h3><label>选择写法 <select class="alias-mode"><option value="share">b = a（共享）</option><option value="copy">b = a.copy()（复制外层）</option></select></label><div class="lab-screen" aria-live="polite"></div><div class="lab-actions"><button data-step="-1">上一步</button><button data-step="1">下一步</button><button data-reset>重新开始</button></div><p class="muted">本演示的列表元素是整数；嵌套列表的浅拷贝请继续看示例 07_05。</p></section>',
9: '<section class="lab" data-lab="function"><div class="eyebrow">动手看调用与返回</div><h3>answer = add(2, 3) 经历了什么</h3><div class="lab-screen" aria-live="polite"></div><div class="lab-actions"><button data-step="-1">上一步</button><button data-step="1">下一步</button><button data-reset>重新开始</button></div><p class="muted">观察参数如何进入函数，返回值如何交回调用位置。</p></section>'}

search=[]; chapters_html=[]; all_md=[]
for c in CHAPTERS:
    n=c['number']; cid=f'c{n:02d}'
    title=f'{n:02d} {c["title"]}'
    metadata = f'{len(c["examples"])} 个示例 · {len(c["exercises"])} 道练习' if c['examples'] else {0:'安装与使用指南 · 从零开始',17:'4 个完整项目 · 从需求到验收',18:'八周路线 · 复习与综合自测'}[n]
    search.append({'target':cid,'title':title,'text':c['body'],'kind':'章节'})
    goals='<ul>'+''.join('<li>'+ESC(g)+'</li>' for g in c['goals'])+'</ul>'
    inner=f'<header class="chapter-header"><div class="eyebrow">第一阶段 / CHAPTER {n:02d}</div><h2>{ESC(c["title"])}</h2><p class="lead">{ESC(c["subtitle"])}</p><div class="chapter-meta">{metadata}</div></header><section class="goals"><h3>本章学会什么</h3>{goals}</section>'
    if n==0:
        inner='<div class="course-intro"><div class="eyebrow">OFFLINE LEARNING KIT · v1.0</div><h1>从零开始<br><span>学会 Python 实操</span></h1><p>逐步理解语法，亲手完成练习。<br>为深度学习与大模型学习打好第一层基础。</p><div class="hero-stats"><span><b>19</b>个学习单元</span><span><b>91</b>个运行示例</span><span><b>100</b>道分层习题</span><span><b>4</b>个完整项目</span></div><a class="primary-link" href="#c01">已装好 Python，开始第一课 →</a><p class="muted">Windows / Mac · 阅读完全离线 · 运行练习需 Python 3.10+</p></div>'+inner
    inner+=md(c['body'],cid)
    if n in SIMS: inner+=SIMS[n]
    chapter_md=f'# {title}\n\n{c["subtitle"]}\n\n## 学习目标\n\n'+''.join('- '+g+'\n' for g in c['goals'])+'\n'+c['body']+'\n'
    if c['examples']: inner+='<h3 class="section-break">示例实验室</h3><p>先预测，再运行，再完成每例后的改写任务。输入栏是运行时需键入的内容，不要写入代码文件。</p>'
    for e in c['examples']:
        target=cid+'-example-'+e['id']
        input_block='<h5>运行时输入（逐行键入）</h5>'+codeblock(e['stdin'],'键盘输入',False) if e['stdin'] else ''
        inner+=f'<section class="example" id="{target}"><div class="item-number">示例 {e["id"]}</div><h4>{ESC(e["title"])}</h4><p class="fileline">运行文件：<a href="{e["path"]}" download>{e["path"]}</a></p>{input_block}{codeblock(e["code"])}<details class="output"><summary>预测完后，查看预期输出</summary>{codeblock(e["output"],"程序输出",False)}</details><h5>怎么执行</h5><p>{ESC(e["explain"])}</p><p class="try"><strong>动手改写：</strong>{ESC(e["challenge"])}</p></section>'
        search.append({'target':target,'title':e['id']+' '+e['title'],'text':e['explain']+' '+e['code'],'kind':'示例'})
        chapter_md+='\n## 示例 '+e['id']+' '+e['title']+'\n\n路径：'+e['path']+'\n\n```python\n'+e['code']+'```\n\n'+('输入：\n```text\n'+e['stdin']+'```\n\n' if e['stdin'] else '')+'输出：\n```text\n'+e['output']+'```\n\n解析：'+e['explain']+'\n\n改写：'+e['challenge']+'\n'
    if c['exercises']: inner+='<h3 class="section-break">独立练习</h3><p>先在 practice 中作答；提示和答案默认收起。勾选表示你已独立完成，不是自动判定通过。</p>'
    for e in c['exercises']:
        target=cid+'-exercise-'+e['id']; check='exercise:'+e['id']
        inp='<h5>自检器提供的输入</h5>'+codeblock(e['stdin'],'输入',False) if e['stdin'] else ''
        extra='<p class="muted">本题含额外函数测试，请使用题目指定的函数或类名。</p>' if e['tests'] else ''
        inner+=f'<section class="exercise" id="{target}"><div class="exercise-top"><span class="item-number">练习 {e["id"]} · {ESC(e["level"])}</span><label class="done-check"><input type="checkbox" data-check="{check}"> 我已独立完成</label></div><h4>{ESC(e["title"])}</h4><p>{ESC(e["task"])}</p><p class="fileline">作答文件：<a href="{e["path"]}" download>{e["path"]}</a></p>{inp}<h5>预期输出</h5>{codeblock(e["output"],"程序输出",False)}{extra}<details><summary>给我一点提示</summary><p>{ESC(e["hint"])}</p></details><details class="solution"><summary>查看参考代码与解析</summary>{codeblock(e["code"])}<h5>解题思路</h5><p>{ESC(e["explain"])}</p><p><a href="{e["solution"]}" download>保存参考答案 .py</a> · 看过后，明天关掉答案重写一次。</p></details><p class="check-command">自检：<code>python tools/check_practice.py {e["id"]}</code></p></section>'
        search.append({'target':target,'title':e['id']+' '+e['title'],'text':e['task']+' '+e['explain'],'kind':'习题'})
        chapter_md+='\n## 练习 '+e['id']+' '+e['title']+'（'+e['level']+'）\n\n'+e['task']+'\n\n作答文件：'+e['path']+'\n\n提示：'+e['hint']+'\n\n参考答案：\n```python\n'+e['code']+'```\n\n输出：\n```text\n'+e['output']+'```\n\n解析：'+e['explain']+'\n'
    if n==17:
        inner+=''.join(project_html); chapter_md+='\n\n'+'\n\n'.join(project_text)
    recall='<ul>'+''.join('<li>'+ESC(t)+'</li>' for t in c['recall'])+'</ul>'
    checkpoint='<ul>'+''.join('<li>'+ESC(t)+'</li>' for t in c['checkpoint'])+'</ul>'
    inner+=f'<section class="recall"><h3>合上教材，回忆这几句</h3>{recall}<h4>本章通关检查</h4>{checkpoint}<label class="chapter-done"><input type="checkbox" data-check="chapter:{n:02d}"> 我已经能独立做到以上要求</label></section><section class="notes"><h3>我的错题与理解</h3><p>写下“我原来以为……，运行后发现……，因为……”。笔记随导出进度保存；代码请保存在 .py 文件。</p><textarea aria-label="第 {n:02d} 章笔记" data-note="{n:02d}" maxlength="20000" placeholder="日期 / 题号 / 错因 / 修正 / 下次复习"></textarea></section>'
    inner+='<nav class="page-nav" aria-label="章节翻页">'+(f'<a href="#c{n-1:02d}">← 上一章</a>' if n else '<span></span>')+(f'<a href="#c{n+1:02d}">下一章 →</a>' if n<18 else '<a href="#c00">回到学习入口 ↑</a>')+'</nav>'
    chapters_html.append(f'<article class="chapter" id="{cid}" {"hidden" if n else ""}>{inner}</article>')
    all_md.append(chapter_md+'\n## 记忆要点\n'+''.join('- '+s+'\n' for s in c['recall'])+'\n## 通关检查\n'+''.join('- '+s+'\n' for s in c['checkpoint']))
write('textbook.md','# Python 零基础实操教程\n\n> Leon · Python — Zero to Practice\n\n版本 1.0 · 2026-10-07 · Windows / Mac\n\n'+ '\n\n'.join(all_md))
nav=''.join(f'<a href="#c{c["number"]:02d}" data-nav="{c["number"]:02d}"><span class="nav-number">{c["number"]:02d}</span><span>{ESC(c["title"])}</span><span class="nav-done" aria-hidden="true"></span></a>' for c in CHAPTERS)
style=(Path(__file__).parent/'style.css').read_text()
script=(Path(__file__).parent/'app.js').read_text()
index_json=json.dumps(search,ensure_ascii=False).replace('</','<\\/')
page=f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light dark"><title>Python 零基础实操教程</title><style>{style}</style></head>
<body><a class="skip-link" href="#reading">跳到正文</a><header class="mobile-header"><b>Python 自学手册</b><button id="toggle-nav" aria-expanded="false" aria-controls="sidebar">目录与搜索</button></header>
<aside id="sidebar"><a class="brand" href="#c00"><span class="brand-mark">Py</span><span>Python 自学手册<small>从第一行代码到独立项目</small></span></a><label class="search-label" for="search">查找知识点或题号</label><input id="search" type="search" placeholder="试试：return、浅拷贝、09_02"><div id="search-results" hidden aria-live="polite"></div><nav id="chapter-nav" aria-label="课程目录">{nav}</nav><div class="sidebar-bottom"><div id="progress-label">已完成 0 / 19 章</div><progress id="progress" max="19" value="0" aria-label="章节学习进度"></progress><div id="exercise-progress">独立完成 0 / 100 题</div><p>本地保存 · 换电脑前请导出进度</p></div></aside>
<main id="reading"><div class="toolbar"><span id="breadcrumb">学习入口</span><div><button id="theme">切换深浅色</button><button id="export-progress">导出进度</button><button id="import-progress">导入进度</button><button id="print">打印本章</button></div></div><p id="storage-warning" hidden>浏览器未允许本地保存；笔记仍可在本次使用中编辑，请手动导出进度。</p><input id="import-file" type="file" accept=".json,application/json" hidden><div id="status" role="status" aria-live="polite"></div><noscript><p>请启用浏览器 JavaScript 来切换章节，或阅读同目录的 textbook.md 文字备份。</p></noscript>{''.join(chapters_html)}<footer>Python 零基础实操教程 · v1.0 · 离线学习包<br>代码在本机 Python 中运行。基础课程无需第三方包。</footer></main><script type="application/json" id="search-data">{index_json}</script><script>{script}</script></body></html>'''
# Leon integration: keep the supplied teaching and learning-state keys.
site_url = 'https://leon1111-wgl.github.io/leon1111-wgl/'
portal = '<nav class="guoliang-portal" aria-label="Leon 学习资料"><a href="'+site_url+'"><strong>Leon</strong> · 学习主页 ↗</a><a href="'+site_url+'downloads/Python-Zero-to-Practice.zip" download>下载完整学习包 ↓</a><a href="textbook.md" download>文字版讲义 ↓</a></nav>'
page = page.replace('<title>Python 零基础实操教程</title>', '<title>Python — Zero to Practice | Leon</title><meta name="description" content="Leon 的 Python 中文自学教程：19 个单元、91 个示例、100 道自学练习和 4 个完整项目。">')
page = page.replace('<main id="reading">', '<main id="reading">'+portal)
page = page.replace('第一阶段 / CHAPTER', 'LEON / CHAPTER')
page = page.replace('OFFLINE LEARNING KIT · v1.0', 'LEON / PYTHON · ZERO TO PRACTICE')
page = page.replace('<footer>Python 零基础实操教程', '<footer><strong>Leon</strong> · Python 零基础实操教程')
route = '<nav class="guoliang-route" aria-label="学习路线"><h3>学习路线</h3><ol><li><a href="#c00">01 · 安装与运行</a></li><li><a href="#c01">02 · 语法与控制</a></li><li><a href="#c07">03 · 容器与函数</a></li><li><a href="#c12">04 · 文件与工程</a></li><li><a href="#c17">05 · 四个完整项目</a></li></ol></nav>'
page = page.replace('<a class="primary-link" href="#c01">', route+'<a class="primary-link" href="#c01">')
write('index.html',page)
write('README_先读我.txt',f'''Leon · Python 零基础实操教程 v1.0

1. 完整解压，再双击 index.html，在浏览器阅读。
2. 第 00 章包含 Windows 与 Mac 的 Python 安装、编辑、运行步骤。
3. 阅读不需网络；运行 .py 需要 Python 3.10+。本教材只用标准库。
4. examples 是可运行示例；practice 是作答区；solutions 是参考答案。
5. projects 包含四个完整项目，先读各项目的 TASKS.md。
6. 换电脑：复制整个文件夹，另行导出并导入网页进度；.venv 应重建。
7. 不要在 ZIP 预览中编辑或运行文件，先解压。不要用 Word 编辑 .py。

教材规模：{len(CHAPTERS)} 个单元，{len(EXAMPLES)} 个示例，{len(EXERCISES)} 道习题，{len(PROJECTS)} 个项目。
从学习包根目录运行（Windows 用 py，Mac 用 python3 替换 python）：
  python examples/ch01/ex01_01.py
  python tools/check_practice.py 01_01
  python tools/check_practice.py --chapter 09
  python tools/verify_examples.py
  python tools/check_projects.py

练习自检会执行你自己编写的本地练习文件，每题限时 5 秒，防止常见无限循环持续卡住。
它不是隔离运行未知代码的安全沙箱；只检查你自己可信的练习。
网页不运行任意 Python，代码复制后需在编辑器保存并运行。
自检输出中不含你在终端键入字符的键盘回显。

开始建议：今天完成第 00—01 章并独立做前 3 题，次日关掉答案重写。
文字备份：textbook.md。编辑源稿：source/；source/build.py 可重新生成教材，保留已有练习文件。
''')
write('notes/错题本.md','''# 我的 Python 错题本

每题记录：

- 日期与题号：
- 我原来预计：
- 实际输出或完整报错：
- 最小复现代码：
- 错误原因（用自己的话）：
- 修正方案：
- 新增的边界测试：
- 次日闭卷重做结果：
- 一周后迁移到新场景的结果：
''',preserve=True)
write('notes/学习记录.csv','date,chapter,exercise,minutes,difficulty,next_review\n',preserve=True)
write('notes/跨电脑迁移清单.txt','''离开旧电脑前
[ ] 保存编辑器中所有 .py 文件
[ ] 网页点击导出进度，将 JSON 与学习包放在一起
[ ] 复制整个学习包，包括 practice、projects、notes
[ ] 有第三方依赖时另存依赖清单，不复制旧 .venv

来到新电脑后
[ ] 安装适合系统的 Python 3.10+
[ ] 完整解压；双击 index.html
[ ] 点击导入进度，选择之前的 JSON（会替换当前网页进度，请先备份）
[ ] 按第 00 章运行一个示例；需要时重建虚拟环境
''')
print(json.dumps({'chapters':len(CHAPTERS),'examples':len(EXAMPLES),'exercises':len(EXERCISES),'projects':len(PROJECTS),'html_bytes':len(page.encode())},ensure_ascii=False))
