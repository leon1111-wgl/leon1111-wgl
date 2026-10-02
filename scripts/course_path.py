"""Course-specific scaffolding for the COMP2017 engineering path."""
from pathlib import Path
from html import escape as E
import json
from teaching import local,paragraphs
from build_projects import projects,page_name
ROOT=Path(__file__).resolve().parents[1]
def path_for(c):
    return json.loads((ROOT/'content/comp2017-path.json').read_text()) if c['code']=='COMP2017' else None

def coach(c,t,lang):
    path=path_for(c)
    if not path:return ''
    x=path['coaches'][t['id']];tr=lambda x:local(x,lang)
    label='A starting model' if lang=='en' else '先建立一个简单模型'
    optional=('Deeper branch · revisit after your first project' if lang=='en' else '深入分支 · 可在第一个工程后回看') if t['id'] in path['deeper'] else ('Core building block' if lang=='en' else '核心基础')
    return '<section class="chapter-coach"><span class="eyebrow">'+optional+'</span><h3>'+label+'</h3>'+paragraphs(tr(x['model']))+'<h4>'+('Use it in an engineering decision' if lang=='en' else '把它用在工程决策里')+'</h4>'+paragraphs(tr(x['engineering']))+'<details class="check"><summary>'+E(tr(x['question']))+'</summary>'+paragraphs(tr(x['answer']))+'</details></section>'

def coach_md(c,t,lang):
    path=path_for(c)
    if not path:return ''
    x=path['coaches'][t['id']];tr=lambda v:local(v,lang)
    return '### '+('Start here, then build' if lang=='en' else '先理解，再构建')+'\n\n'+tr(x['model'])+'\n\n'+tr(x['engineering'])+'\n\n**'+tr(x['question'])+'**\n\n'+tr(x['answer'])

def path_html(c,lang):
    path=path_for(c)
    if not path:return ''
    tr=lambda v:local(v,lang);topics={t['id']:t['title'] for t in c['topics']};projs={p['id']:p for p in projects()}
    html='<section class="study-path" id="study-plan" data-reading-id="study-plan"><div class="route-heading"><div><span class="eyebrow">GUOLIANG / COMP2017 / START HERE</span><h2>'+E(tr(path['title']))+'</h2></div></div>'+paragraphs(tr(path['intro']))+'<ol class="study-passes">'
    for i,s in enumerate(path['sessions'],1):
        html+='<li><span class="route-step">'+f'{i:02d}'+'</span><h3>'+E(tr(s['title']))+'</h3>'+paragraphs(tr(s['goal']))+'<a class="text-link" href="#'+s['topics'][0]+'">'+('Start this pass' if lang=='en' else '开始这一轮')+' →</a><details><summary>'+('Chapters and readiness check' if lang=='en' else '章节与过关检查')+'</summary><ul>'+''.join('<li><a href="#'+id+'">'+E(topics[id])+'</a></li>' for id in s['topics'])+'</ul><p><strong>'+('Ready when: ' if lang=='en' else '过关标准：')+'</strong>'+E(tr(s['checkpoint']))+'</p></details>'
        if s['project'] in projs:html+='<a class="project-next" href="../projects/'+page_name(projs[s['project']],lang)+'">'+('Build the project' if lang=='en' else '动手完成工程')+' ↗</a>'
        html+='</li>'
    html+='</ol></section><section class="project-library" id="projects" data-reading-id="projects"><div class="route-heading"><div><span class="eyebrow">GUOLIANG / ENGINEERING WORKSHOPS</span><h2>'+('From small examples to complete tools' if lang=='en' else '从小例子走向完整工具')+'</h2></div><p>'+('Open a project for requirements, architecture, staged explanations, complete source, debugging and tests.' if lang=='en' else '打开工程，阅读需求、结构、分步讲解、完整源码、调试过程与测试。')+'</p></div><div class="project-cards">'
    for p in projs.values():
        html+='<a class="project-card" href="../projects/'+page_name(p,lang)+'"><span class="eyebrow">PROJECT '+f'{p["number"]:02d}'+'</span><h3>'+E(tr(p['title']))+'</h3>'+paragraphs(tr(p['summary']))+'<span class="project-next">'+E(tr(p['difficulty']))+' ↗</span></a>'
    html+='</div><p><a class="text-link" href="../downloads/COMP2017-projects.zip" download>'+('Download all three complete projects' if lang=='en' else '下载全部三个完整工程')+' ↓</a></p></section>'
    return html

def path_md(c,lang):
    path=path_for(c)
    if not path:return ''
    tr=lambda v:local(v,lang);topics={t['id']:t['title'] for t in c['topics']};projs={p['id']:p for p in projects()}
    md=['## '+tr(path['title']),tr(path['intro'])]
    for i,s in enumerate(path['sessions'],1):
        md+=['### '+f'{i:02d} / '+tr(s['title']),tr(s['goal'])]+[f'- [{topics[id]}](#{id})' for id in s['topics']]+[tr(s['checkpoint'])]
        if s['project'] in projs:
            p=projs[s['project']];md+=[f'[{tr(p["title"])}](../projects/{page_name(p,lang)})']
    md+=['## '+('Complete engineering workshops' if lang=='en' else '完整工程讲解')]+[f'- [{tr(p["title"])}](../projects/{page_name(p,lang)}): '+tr(p['summary']) for p in projs.values()]
    return '\n\n'.join(md)
