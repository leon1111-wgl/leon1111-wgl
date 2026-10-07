"""Build complete bilingual engineering workshops and exact source archives."""
from pathlib import Path
from html import escape as E
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED
import json
from teaching import local, paragraphs, code_html, asset_version
from roadmaps import build_roadmap
ROOT=Path(__file__).resolve().parents[1]; SITE=ROOT/'site'

def projects():
    return sorted((json.loads(p.read_text()) for p in (ROOT/'content/projects').glob('comp2017-*.json')),key=lambda p:p['number'])

def page_name(p,lang):return p['id']+'.'+lang+'.html'
def L(lang,en,zh):return zh if lang=='zh' else en

def source(p,f):
    path=Path(f['path'])
    if path.is_absolute() or '..' in path.parts:raise ValueError('Unsafe project source path')
    return (ROOT/'projects'/p['id']/path).read_bytes().decode('utf-8')

def file_id(path):return 'file-'+''.join(c if c.isalnum() else '-' for c in path)
def full_source_html(text,path,id):
    # Data fixtures can be entirely whitespace. Preserve CR as a character
    # reference so the browser does not normalize CRLF while parsing HTML.
    if path.startswith('fixtures/') and Path(path).suffix not in {'.c','.h'}:
        raw=E(text).replace('\r','&#13;')
        return f'<pre class="code highlighted" tabindex="0"><code id="{E(id)}" class="language-text">{raw}</code></pre>'
    return code_html(text,lexer(path),id)

def lexer(path):
    name=Path(path).name
    return 'make' if name=='Makefile' else {'.c':'c','.h':'c','.py':'python','.sh':'bash','.md':'text'}.get(Path(path).suffix,'text')

def shell(p,lang,body):
    links=''.join(f'<a href="{page_name(p,l)}" data-language="{l}" lang="{l}"'+(' aria-current="page"' if l==lang else '')+f'>{name}</a>' for l,name in [('en','EN'),('zh','中文')])
    title=local(p['title'],lang);iso='zh-Hans' if lang=='zh' else 'en'
    return f'''<!doctype html><html lang="{iso}" data-theme="dark"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)} | Leon</title><meta name="description" content="{E(local(p['summary'],lang))}"><link rel="icon" href="../assets/favicon.svg"><link rel="stylesheet" href="../assets/style.css?v={asset_version('style.css')}"><script defer src="../assets/app.js?v={asset_version('app.js')}"></script></head><body class="field-guide project-guide"><a class="skip" href="#main">{L(lang,'Skip to content','跳到正文')}</a><header class="topbar"><div class="wrap"><a class="brand" href="../index.html"><span class="monogram">LW</span>Leon</a><nav><a href="../courses/comp2017{'.zh' if lang=='zh' else ''}.html#projects">COMP2017</a><div class="language-switch">{links}</div><button type="button" class="theme-button" data-theme-toggle aria-label="Switch to light theme">☼</button></nav></div></header><main id="main" class="wrap">{body}<footer class="footer"><span class="watermark">Leon</span><a href="../courses/comp2017{'.zh' if lang=='zh' else ''}.html#projects">{L(lang,'Back to the engineering path','返回工程学习路线')} ↑</a></footer></main></body></html>'''

def archive(path,entries):
    with ZipFile(path,'w',ZIP_DEFLATED,compresslevel=9) as z:
        for name,data in sorted(entries.items()):
            info=ZipInfo(name,(2026,10,3,0,0,0));info.compress_type=ZIP_DEFLATED;info.external_attr=0o644<<16
            z.writestr(info,data)

def build_one(p,lang):
    tr=lambda x:local(x,lang)
    course_data=ROOT/'content'/('translations/COMP2017.zh.json' if lang=='zh' else 'COMP2017.json')
    topic_titles={t['id']:t['title'] for t in json.loads(course_data.read_text())['topics']}
    P=lambda x:paragraphs(tr(x))
    heading=lambda id,title: f'<section class="project-section" id="{id}"' + (f' data-reading-id="{id}"' if id != "source" else "") + f'><h2>{title}</h2>'
    doc={'code':p['id'],'title':p['title'],'map':[{'title':m['title'],'topics':[m['id']],'count_label':{'en':'Build · explain · check','zh':'构建 · 解释 · 检查'}} for m in p['milestones']]}
    map_path=build_roadmap(doc,lang)
    route='<section class="learning-route" aria-labelledby="route-title"><div class="route-heading"><div><span class="eyebrow">LEON / BUILD ROUTE</span><h2 id="route-title">'+L(lang,'Build one working piece at a time','每次完成一个可运行的小部分')+'</h2></div></div><ol class="route-flow">'+''.join(f'<li><a class="route-node" href="#milestone-{m["id"]}"><span class="route-step">{i:02d} →</span><h3>{E(tr(m["title"]))}</h3><p>{E(tr(m["goal"]))}</p></a></li>' for i,m in enumerate(p['milestones'],1))+'</ol></section>'
    title=tr(p['title']);note=p['id']+'.'+lang+'.md'
    course='../courses/comp2017'+('.zh' if lang=='zh' else '')+'.html'
    setup=f'unzip {p["id"]}.zip\ncd {p["id"]}\nmake\nmake test'
    environment=L(lang,'Use Clang with C11 support, make and Python 3 on macOS or Linux. On Windows use a Linux environment such as WSL. The supplied Makefiles use Clang. Open a terminal in the download directory. Unzip the archive, then enter its folder. make builds the executable; make test checks its behavior.','使用 macOS 或 Linux 上支持 C11 的 Clang、make 和 Python 3。Windows 可使用 WSL 等 Linux 环境。这里的 Makefile 默认使用 Clang。在下载目录打开终端，解压并进入工程文件夹。make 构建可执行文件；make test 检查程序行为。')
    body=f'<header class="course-hero"><div class="eyebrow">LEON / COMP2017 / PROJECT {p["number"]:02d}</div><h1>{E(title)}</h1>{P(p["summary"])}<p class="course-meta">{E(tr(p["difficulty"]))} · C11 / POSIX · EN / ZH</p><div class="actions"><a class="button primary" href="../downloads/{p["id"]}.zip" download>{L(lang,"Download the complete project","下载完整工程")} ↓</a><a class="button" href="#source">{L(lang,"Read every source file","阅读完整源文件")} ↓</a><a class="button" href="../notes/{note}" download>{L(lang,"Download this guide","下载本篇讲义")} ↓</a></div></header>'+route
    body+='<div class="reading-tools"><div role="group" aria-label="'+L(lang,'Text size','阅读字号')+'"><span>'+L(lang,'Text size','阅读字号')+'</span><button type="button" data-reading-size="normal" aria-pressed="true">A · '+L(lang,'Comfortable','舒适')+'</button><button type="button" data-reading-size="large" aria-pressed="false">A+ · '+L(lang,'Larger','更大')+'</button></div><a href="#run">'+L(lang,'Build and run this project','构建并运行这个工程')+' ↓</a></div>'
    nav=[('story',L(lang,'The problem','问题从哪里来')),('contract',L(lang,'Requirements and contracts','需求与契约')),('architecture',L(lang,'Architecture and ownership','结构与所有权'))]+[('milestone-'+m['id'],tr(m['title'])) for m in p['milestones']]+[('run',L(lang,'Build and run','构建与运行')),('debug',L(lang,'Find and explain failures','定位并解释错误')),('test',L(lang,'Test the contracts','验证契约')),('decisions',L(lang,'Engineering decisions','工程取舍')),('source',L(lang,'Complete source','完整源文件')),('next',L(lang,'Extend deliberately','有计划地扩展'))]
    body+='<div class="course-layout"><aside class="toc"><details open><summary>'+L(lang,'PROJECT GUIDE','工程学习目录')+'</summary><ol>'+''.join(f'<li><a href="#{id}">{E(t)}</a></li>' for id,t in nav)+'</ol></details></aside><div class="course-body">'
    md=[f'# COMP2017 — {title}','> Leon | Original engineering workshop',f'![Leon learning route]({map_path})',f'[English]({p["id"]}.en.md) · [中文]({p["id"]}.zh.md)',tr(p['summary']),f'[{L(lang,"Download the complete project ZIP","下载完整工程 ZIP")}](../downloads/{p["id"]}.zip)']
    body+=heading('story',L(lang,'Start with a complete story','从一个完整故事开始'))+P(p['story'])+'<h3>'+L(lang,'Before this project','开始前先读')+'</h3><ul>'+''.join(f'<li><a href="{course}#{x["topic"]}">{E(topic_titles[x["topic"]])}</a> — {E(tr(x["reason"]))}</li>' for x in p['prerequisites'])+'</ul><h3>'+L(lang,'By the end, you can','完成后你能够')+'</h3><ul>'+''.join('<li>'+E(tr(x))+'</li>' for x in p['outcomes'])+'</ul></section>'
    md+=['## '+L(lang,'The story','故事'),tr(p['story']),'### '+L(lang,'Before this project','开始前先读')]+[f'- [{topic_titles[x["topic"]]}]({course}#{x["topic"]}): '+tr(x['reason']) for x in p['prerequisites']]+['### '+L(lang,'Outcomes','学习成果')]+['- '+tr(x) for x in p['outcomes']]
    body+=heading('contract',L(lang,'Make requirements testable','把需求写成可检查的行为'))
    md+=['## '+L(lang,'Requirements and contracts','需求与契约')]
    for x in p['requirements']:
        body+='<article class="design-card"><h3>'+E(tr(x['rule']))+'</h3>'+P(x['why'])+'<p><strong>'+L(lang,'Check: ','检查方法：')+'</strong>'+E(tr(x['check']))+'</p></article>'
        md+=['### '+tr(x['rule']),tr(x['why']),tr(x['check'])]
    body+='</section>'+heading('architecture',L(lang,'Follow the data and its owner','追踪数据和它的所有者'))+'<ol class="architecture-flow">'+''.join('<li><h3>'+E(tr(n['title']))+'</h3>'+P(n['body'])+'</li>' for n in p['architecture']['nodes'])+'</ol>'+P(p['architecture']['flow'])
    body+='<div class="trace-wrap" tabindex="0"><table class="trace-table"><caption>'+L(lang,'Who owns each resource?','谁负责每一种资源？')+'</caption><thead><tr>'+''.join('<th scope="col">'+s+'</th>' for s in (["Resource","Owner","Release"] if lang=='en' else ['资源','所有者','释放时机']))+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+E(tr(x[k]))+'</td>' for k in ['resource','owner','release'])+'</tr>' for x in p['architecture']['ownership'])+'</tbody></table></div></section>'
    md+=['## '+L(lang,'Architecture and ownership','结构与所有权')]+['**'+tr(n['title'])+'**\n\n'+tr(n['body']) for n in p['architecture']['nodes']]+[tr(p['architecture']['flow'])]+['- '+tr(x['resource'])+' → '+tr(x['owner'])+' → '+tr(x['release']) for x in p['architecture']['ownership']]
    for i,m in enumerate(p['milestones'],1):
        body+=heading('milestone-'+m['id'],f'{i:02d} / '+E(tr(m['title'])))+'<div class="milestone-goal">'+P(m['goal'])+'</div>'+P(m['reasoning'])+'<ol class="execution-steps">'+''.join('<li>'+P(x)+'</li>' for x in m['steps'])+'</ol><p class="code-hint">'+L(lang,'Teaching extract from the complete project. Build the full files below to run it.','这是完整工程中的教学摘录。请构建下面的完整文件后运行。')+'</p>'+code_html(m['snippet']['code'],m['snippet']['language'],'project-snippet-'+m['id'])+P(m['snippet_explanation'])+'<details class="check"><summary>'+E(tr(m['checkpoint']['question']))+'</summary>'+P(m['checkpoint']['answer'])+'</details></section>'
        md+=['<a id="milestone-'+m['id']+'"></a>','## '+tr(m['title']),tr(m['goal']),tr(m['reasoning'])]+[f'{j}. '+tr(x) for j,x in enumerate(m['steps'],1)]+[L(lang,'Teaching extract; run the complete project.','教学摘录；运行时使用完整工程。'),'```'+m['snippet']['language']+'\n'+m['snippet']['code'].rstrip()+'\n```',tr(m['snippet_explanation']),'**'+tr(m['checkpoint']['question'])+'**',tr(m['checkpoint']['answer'])]
    body+=heading('run',L(lang,'Build it, run it, read the result','构建、运行并读懂结果'))+'<p>'+E(environment)+'</p>'+code_html(setup,'bash')
    md+=['## '+L(lang,'Build and run','构建与运行'),environment,'```sh\n'+setup+'\n```']
    for x in p['runs']:
        status=L(lang,'Exit status: ','退出状态：')+str(x['expected_exit'])
        empty=L(lang,'No standard output. Read the exit status and any diagnostic on stderr.','没有标准输出。请查看退出状态以及标准错误中的诊断信息。') if not x['stdout'] else ''
        body+='<article class="code-example"><h3>'+E(tr(x['title']))+'</h3>'+code_html(x['command'],'bash')+'<div class="output-block"><h4>'+L(lang,'Expected stdout','预期标准输出')+'</h4><pre class="code code-output">'+E(x['stdout'])+'</pre></div><p class="code-hint">'+E(status)+'. '+empty+'</p>'+P(x['explanation'])+'</article>'
        md+=['### '+tr(x['title']),'```sh\n'+x['command']+'\n```','```text\n'+x['stdout'].rstrip()+'\n```',status,empty,tr(x['explanation'])]
    body+='</section>'+heading('debug',L(lang,'Debug from evidence','依据现象定位错误'));md+=['## '+L(lang,'Debugging','调试')]
    for x in p['debugging']:
        body+='<article class="design-card"><h3>'+E(tr(x['symptom']))+'</h3>'+''.join('<h4>'+label+'</h4>'+P(x[k]) for k,label in [('hypothesis',L(lang,'Form a hypothesis','提出假设')),('inspection',L(lang,'Inspect the right state','检查相关状态')),('fix',L(lang,'Repair and verify','修复并验证'))])+'</article>'
        md+=['### '+tr(x['symptom'])]+[tr(x[k]) for k in ['hypothesis','inspection','fix']]
    body+='</section>'+heading('test',L(lang,'Test behavior, including failure','验证正常行为，也验证失败'))+'<div class="test-cases">';md+=['## '+L(lang,'Test plan','测试计划')]
    for x in p['test_plan']:
        body+='<article class="design-card"><h3>'+E(tr(x['case']))+'</h3>'+P(x['expected'])+P(x['reason'])+'</article>';md+=['### '+tr(x['case']),tr(x['expected']),tr(x['reason'])]
    body+='</div></section>'+heading('decisions',L(lang,"Leon's engineering decisions",'Leon 的工程取舍'));md+=['## '+L(lang,'Engineering decisions','工程取舍')]
    for x in p['design_notes']:
        body+='<article class="design-card"><h3>'+E(tr(x['title']))+'</h3>'+P(x['body'])+'</article>';md+=['### '+tr(x['title']),tr(x['body'])]
    body+='</section>'+heading('source',L(lang,'Read the complete files in order','按顺序阅读完整文件'))+'<p>'+L(lang,'These are the complete files in the download. The numbers suggest a reading order. The file list links directly to each source block.','下面是下载包中的完整文件。编号表示建议阅读顺序。点击文件清单可直接跳转到代码。')+'</p><ul class="file-index">'+''.join(f'<li><a href="#{file_id(f["path"])}">{f["read_order"]:02d} / {E(f["path"])}</a></li>' for f in sorted(p['files'],key=lambda f:f['read_order']))+'</ul>'
    md+=['## '+L(lang,'Complete source files','完整源文件')]
    for f in sorted(p['files'],key=lambda f:f['read_order']):
        text=source(p,f);id=file_id(f['path']);url='../project-code/'+p['id']+'/'+f['path']
        byte_hint=(L(lang,'Invisible-byte view (hexadecimal): ','不可见字节视图（十六进制）：')+(text.encode().hex(' ') or L(lang,'empty file; zero bytes','空文件；零字节'))) if not text.strip() else ''
        body+=f'<article class="code-example project-file" id="{id}" data-reading-id="{id}"><h3>{f["read_order"]:02d} / {E(f["path"])}</h3>'+P(f['role'])+f'<div class="code-actions"><button type="button" data-copy-code="code-{id}">'+L(lang,'Copy file','复制文件')+f'</button><a href="{E(url)}" download>'+L(lang,'Download file','下载文件')+' ↓</a><p class="code-hint">'+L(lang,'Keep these file names and folders when building. Long lines scroll within the code panel.','构建时请保留文件名和目录结构。长行在代码框内横向滚动。')+'</p></div>'+full_source_html(text,f['path'],'code-'+id)+(('<p class="code-hint">'+E(byte_hint)+'</p>') if byte_hint else '')+'<ol class="execution-steps">'+''.join('<li>'+P(x)+'</li>' for x in f['walkthrough'])+'</ol></article>'
        md+=['### '+f['path'],tr(f['role']),f'[{L(lang,"Download file","下载文件")}]({url})']
        # README files contain their own Markdown fences; link them above.
        if byte_hint:md+=[byte_hint]
        elif Path(f['path']).suffix!='.md':md+=['```'+lexer(f['path'])+'\n'+text+('' if text.endswith('\n') else '\n')+'```']
        md += [f'{i}. '+tr(x) for i,x in enumerate(f['walkthrough'],1)]
    body+='</section>'+heading('next',L(lang,'Extend one contract at a time','每次只扩展一项契约'));md+=['## '+L(lang,'Extensions','扩展方向')]
    for x in p['extensions']:
        body+='<article class="design-card"><h3>'+E(tr(x['title']))+'</h3>'+P(x['plan'])+'<h4>'+L(lang,'Acceptance check','验收检查')+'</h4>'+P(x['acceptance'])+'</article>';md+=['### '+tr(x['title']),tr(x['plan']),tr(x['acceptance'])]
    body+='<h3>'+L(lang,'Primary references','一手参考资料')+'</h3><ul>'+''.join(f'<li><a href="{E(r["url"])}">{E(r["title"])}</a></li>' for r in p['references'])+'</ul></section></div></div>'
    md+=['## '+L(lang,'Primary references','一手参考资料')]+[f'- [{r["title"]}]({r["url"]})' for r in p['references']]+['---\nLeon']
    (SITE/'projects'/page_name(p,lang)).write_text(shell(p,lang,body))
    text='\n\n'.join(md)+'\n';(SITE/'notes'/note).write_text(text)
    (ROOT/'notes'/note).write_text(text.replace('](../assets/','](../site/assets/').replace('](../project-code/','](../projects/').replace('](../courses/','](../site/courses/').replace('](../downloads/','](../site/downloads/'))

def build_all():
    for d in ['projects','project-code','downloads','notes']:(SITE/d).mkdir(exist_ok=True)
    combined={}
    for p in projects():
        entries={}
        for f in p['files']:
            data=source(p,f).encode();path=SITE/'project-code'/p['id']/f['path'];path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
            entries[p['id']+'/'+f['path']]=data
        archive(SITE/'downloads'/(p['id']+'.zip'),entries);combined.update(entries)
        for lang in ['en','zh']:build_one(p,lang)
    if combined:archive(SITE/'downloads'/'COMP2017-projects.zip',combined)
    print(f'Built {len(projects())} complete bilingual C engineering projects.')

if __name__=='__main__':build_all()
