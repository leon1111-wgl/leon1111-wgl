"""Accessible course route diagrams, shared by HTML and downloadable notes."""
from html import escape as E
from pathlib import Path
from teaching import local

ROOT = Path(__file__).resolve().parents[1]


def slug(document):
    return document['code'].lower()


def roadmap_html(document, lang='en', prefix=''):
    zh=lang=='zh'
    heading='先看学习路线' if zh else 'See the learning route first'
    intro='按箭头顺序学习。点击一个阶段进入第一节；完整知识框架列出了每一个主题。' if zh else 'Follow the arrows. Choose a stage to open its first lesson. The full framework lists every topic.'
    stages=[]
    for i,stage in enumerate(document['map'],1):
        first=stage['topics'][0]
        purpose=local(stage.get('purpose',''),lang)
        count=f'{len(stage["topics"])} 个主题' if zh else f'{len(stage["topics"])} topics'
        stages.append(f'<li><a class="route-node" href="{prefix}#{first}"><span class="route-step">{i:02d} <span aria-hidden="true">→</span></span><h3>{E(local(stage["title"],lang))}</h3>'+ (f'<p>{E(purpose)}</p>' if purpose else '') +f'<span class="route-count">{count} ↗</span></a></li>')
    return f'<section class="learning-route" aria-labelledby="route-title"><div class="route-heading"><div><span class="eyebrow">GUOLIANG / LEARNING MAP</span><h2 id="route-title">{heading}</h2></div><p>{intro}</p></div><ol class="route-flow">'+''.join(stages)+'</ol></section>'


def wrapped(text, width):
    # CJK glyphs need about twice the horizontal space of Latin letters.
    lines=[];line='';length=0
    for word in text.split(' ') if ' ' in text else list(text):
        cost=sum(2 if ord(c)>0x2fff else 1 for c in word)
        spacer=' ' if ' ' in text else ''
        if line and length+cost+len(spacer)>width:
            lines.append(line);line='';length=0
        line+=(spacer if line else '')+word;length+=cost+len(spacer)
    if line:lines.append(line)
    return lines


def build_roadmap(document,lang='en'):
    stages=document['map'];width=1040;row_height=140;height=154+len(stages)*row_height
    title=local(document['title'],lang)
    title_lines=wrapped(title,66)
    top=96+24*max(0,len(title_lines)-1)
    height=top+50+len(stages)*row_height
    items=['<rect width="1040" height="'+str(height)+'" rx="20" fill="#101925"/>', f'<path d="M90 {top+60}V{height-75}" stroke="#497a83" stroke-width="3"/>']
    items.append('<text x="40" y="38" fill="#abdca0" font-size="17" letter-spacing="2">GUOLIANG / '+E(document['code'])+' / LEARNING ROUTE</text>')
    for i,line in enumerate(title_lines):items.append(f'<text x="40" y="{78+i*30}" fill="#f0f4fa" font-size="28" font-weight="600">{E(line)}</text>')
    for i,stage in enumerate(stages):
        y=top+32+i*row_height
        items.append(f'<rect x="125" y="{y-18}" width="865" height="112" rx="12" fill="#172536" stroke="#385466"/>')
        items.append(f'<circle cx="90" cy="{y+34}" r="24" fill="#abdca0"/><text x="90" y="{y+41}" fill="#14231c" text-anchor="middle" font-size="20" font-weight="700">{i+1:02d}</text>')
        for j,line in enumerate(wrapped(local(stage['title'],lang),62)):
            items.append(f'<text x="150" y="{y+15+j*27}" fill="#f0f4fa" font-size="23">{E(line)}</text>')
        text=local(stage['count_label'],lang) if stage.get('count_label') else (f'{len(stage["topics"])} 个主题' if lang=='zh' else f'{len(stage["topics"])} topics')
        items.append(f'<text x="150" y="{y+77}" fill="#b7c9dc" font-size="18">{text}</text>')
    image=f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title"><title id="title">Guoliang — {E(title)}</title><g font-family="Arial, PingFang SC, Microsoft YaHei, sans-serif">'+''.join(items)+'</g></svg>'
    path=ROOT/'site'/'assets'/'maps'/f'{slug(document)}.{lang}.svg'
    path.parent.mkdir(exist_ok=True,parents=True);path.write_text(image)
    return '../assets/maps/'+path.name


def roadmap_markdown(document,lang='en'):
    image=build_roadmap(document,lang)
    label='学习路线图' if lang=='zh' else 'Learning roadmap'
    return f'![Guoliang — {label}]({image})'
