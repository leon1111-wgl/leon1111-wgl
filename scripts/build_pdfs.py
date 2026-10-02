#!/usr/bin/env python3
"""Render one genuinely single-page, watermarked reference for each course."""
from pathlib import Path
import json,html,math,sys,shutil
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor,Color
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_LEFT
from pypdf import PdfReader,PdfWriter
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'site'/'downloads';OUT.mkdir(parents=True,exist_ok=True)
ALL_ORDER=['INFO1113','COMP2017','COMP2123','COMP2022','COMP3308']
ORDER=sys.argv[1:] or ALL_ORDER
assert set(ORDER).issubset(ALL_ORDER), 'Unknown course code'
FONT_ROOT=Path('/System/Library/Fonts/Supplemental')
for name,filename in [('Guide','DejaVuSans.ttf'),('GuideBold','DejaVuSans-Bold.ttf')]:
 candidates=[ROOT/'scripts'/'fonts'/filename,Path('/usr/share/fonts/truetype/dejavu')/filename]
 path=next((p for p in candidates if p.exists()),None)
 if not path:raise RuntimeError('Missing portable DejaVu fonts in scripts/fonts')
 pdfmetrics.registerFont(TTFont(name,str(path)))
W,H=841.89,595.28
PAPER=HexColor('#f6f8f5');INK=HexColor('#172c28');MUTED=HexColor('#49605a');LINE=HexColor('#d8e2d8');GREEN=HexColor('#326846')
def normalized(s):
 return s.replace('𝑂','O').replace('∑','Σ').replace('𝒪','O').replace('−','-').replace('‑','-').replace('–','-').replace('—','-').replace('⇒','→')
def style(size,bold=False,color=INK):return ParagraphStyle('s',fontName='GuideBold' if bold else 'Guide',fontSize=size,leading=size*1.37,textColor=color,spaceAfter=0)
def draw_p(c,text,x,y,width,size=9,bold=False,color=INK):
 p=Paragraph(html.escape(normalized(text)).replace('\n','<br/>'),style(size,bold,color));_,h=p.wrap(width,1000);p.drawOn(c,x,y-h);return h
metadata=[]
ROUTES={
 'INFO1113':['Trace execution','Object contracts','Data and types','Change and failure','Application design'],
 'COMP2017':['Memory and C','Processes and IPC','Threads and safety','Parallel performance'],
 'COMP2123':['Analysis and structures','Graph algorithms','Greedy proofs','Divide and randomize'],
 'COMP2022':['Finite automata','Grammars and parsing','Computability','Logic and inference'],
 'COMP3308':['Search and games','Learning from data','Neural models','Probability and clusters']}
for code in ORDER:
 course=json.loads((ROOT/'content'/f'{code}.json').read_text());items=course['cheatsheet']
 rows=math.ceil(len(items)/3);gap=10;left=29;right=29;top=H-134;bottom=48
 cw=(W-left-right-gap*2)/3;ch=(top-bottom-gap*(rows-1))/rows
 path=OUT/f'{code}-cheatsheet.pdf';c=canvas.Canvas(str(path),pagesize=(W,H),pageCompression=1)
 c.setTitle(code+' — '+course['title']+' | Guoliang');c.setAuthor('Guoliang Wang');c.setSubject('One-page original computer science study reference')
 c.setFillColor(PAPER);c.rect(0,0,W,H,fill=1,stroke=0)
 c.setFillColor(INK);c.roundRect(left,H-40,27,21,5,fill=1,stroke=0);c.setFillColor(PAPER);c.setFont('GuideBold',9);c.drawCentredString(left+13.5,H-33,'GW')
 c.setFont('GuideBold',9);c.setFillColor(GREEN);c.drawString(left+38,H-32,'GUOLIANG / ONE-PAGE REFERENCE')
 c.setFont('Guide',9);c.setFillColor(MUTED);c.drawRightString(W-right,H-32,code)
 title_size=22
 while pdfmetrics.stringWidth(course['title'],'GuideBold',title_size)>W-left-right:title_size-=.5
 c.setFont('GuideBold',title_size);c.setFillColor(INK);c.drawString(left,H-72,course['title'])
 route_width=(W-left-right-15*(len(ROUTES[code])-1))/len(ROUTES[code])
 for stage,label in enumerate(ROUTES[code]):
  x=left+stage*(route_width+15)
  c.setFillColor(HexColor('#e5eee6'));c.roundRect(x,H-115,route_width,25,5,fill=1,stroke=0)
  c.setFont('GuideBold',8.5);c.setFillColor(GREEN);c.drawString(x+8,H-105,f'{stage+1:02d} / '+label)
  if stage<len(ROUTES[code])-1:c.drawString(x+route_width+3,H-105,'→')
 # Print-friendly original-brand watermark, beneath the foreground content.
 c.saveState();c.translate(W/2,H/2);c.rotate(18);c.setFillColor(Color(.2,.4,.27,alpha=.035));c.setFont('GuideBold',95);c.drawCentredString(0,-30,'Guoliang');c.restoreState()
 minfont=20
 for i,item in enumerate(items):
  col=i%3;row=i//3;x=left+col*(cw+gap);y=top-row*(ch+gap)
  c.setFillColor(HexColor('#ffffff'));c.setStrokeColor(LINE);c.setLineWidth(.6);c.roundRect(x,y-ch,cw,ch,7,fill=1,stroke=1)
  inner=cw-22;size=9.4
  while True:
   hp=Paragraph(html.escape(normalized(f'{i+1:02d} / '+item['title'])),style(size+.4,True,GREEN));_,hh=hp.wrap(inner,1000)
   bp=Paragraph(html.escape(normalized(item['body'])).replace('\n','<br/>'),style(size,False,MUTED));_,bh=bp.wrap(inner,1000)
   if hh+bh+8<=ch-22:break
   size-=.2
   if size<7.6:raise ValueError(f'{code}: block {i} needs editing; too much text')
  minfont=min(minfont,size);hp.drawOn(c,x+11,y-11-hh);bp.drawOn(c,x+11,y-11-hh-8-bh)
 c.saveState();c.translate(W/2,H/2);c.rotate(18);c.setFillColor(Color(.2,.4,.27,alpha=.035));c.setFont('GuideBold',95);c.drawCentredString(0,-30,'Guoliang');c.restoreState()
 c.setStrokeColor(LINE);c.line(left,33,W-right,33);c.setFont('GuideBold',9);c.setFillColor(GREEN);c.drawString(left,18,'Guoliang')
 c.setFont('Guide',7.5);c.setFillColor(MUTED);c.drawCentredString(W/2,18,'STORY → PRINCIPLE → FORMULA → EXAMPLE');c.drawRightString(W-right,18,code+' / 1 PAGE')
 c.showPage();c.save()
 reader=PdfReader(path);assert len(reader.pages)==1
 assert 'Guoliang' in reader.pages[0].extract_text()
 metadata.append({'course':code,'pages':1,'smallest_body_font':round(minfont,1),'blocks':len(items),'filename':path.name})
if set(ORDER)==set(ALL_ORDER):
 writer=PdfWriter()
 for code in ALL_ORDER:writer.append(str(OUT/f'{code}-cheatsheet.pdf'))
 writer.add_metadata({'/Title':'Guoliang — Computer Science Cheatsheet Collection','/Author':'Guoliang Wang'})
 with open(OUT/'guoliang-cheatsheet-collection.pdf','wb') as f:writer.write(f)
FINAL=ROOT/'output'/'pdf';FINAL.mkdir(parents=True,exist_ok=True)
for code in ORDER:shutil.copy2(OUT/f'{code}-cheatsheet.pdf',FINAL/f'{code}-cheatsheet.pdf')
if set(ORDER)==set(ALL_ORDER):shutil.copy2(OUT/'guoliang-cheatsheet-collection.pdf',FINAL/'guoliang-cheatsheet-collection.pdf')
print(json.dumps(metadata,indent=2))
