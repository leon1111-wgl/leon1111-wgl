/* The map uses embedded course data only. Selection is a URL fragment, not progress. */
(() => {
'use strict';
const root = document.getElementById('c00-knowledge-map');
if (!root) return;
const data = JSON.parse(document.getElementById('knowledge-data').textContent);
const nodes = new Map(data.nodes.map(node => [node.id, node]));
const $ = id => document.getElementById(id);
let selected = 'functions';
const text = (tag, value, className) => { const el=document.createElement(tag); el.textContent=value; if(className) el.className=className; return el; };
function nodeLink(id) {
  const link=text('a', nodes.get(id).title);
  link.href='#c00-map-'+id; link.dataset.mapNode=id;
  return link;
}
function relationBox(rel, id) {
  const box=text('div','','map-relation'); box.append(nodeLink(id),text('p',rel.why)); return box;
}
function redraw() {
  const svg=$('map-lines'); svg.replaceChildren();
  if (!root.getClientRects().length || matchMedia('(max-width: 760px)').matches) return;
  const graph=$('map-graph').getBoundingClientRect();
  if (!graph.width) return;
  svg.setAttribute('viewBox',`0 0 ${graph.width} ${graph.height}`);
  const ns='http://www.w3.org/2000/svg';
  const defs=document.createElementNS(ns,'defs');
  const marker=document.createElementNS(ns,'marker');
  marker.id='map-arrow';marker.setAttribute('markerWidth','7');marker.setAttribute('markerHeight','7');marker.setAttribute('refX','6');marker.setAttribute('refY','3.5');marker.setAttribute('orient','auto');
  const head=document.createElementNS(ns,'path');head.setAttribute('d','M0 0 L7 3.5 L0 7');head.setAttribute('fill','var(--accent)');marker.append(head);defs.append(marker);svg.append(defs);
  const center=$('map-current').querySelector('.map-selected').getBoundingClientRect();
  function wire(start,end) {
    const path=document.createElementNS(ns,'path');
    const mid=(start[0]+end[0])/2;
    path.setAttribute('d',`M${start[0]},${start[1]} C${mid},${start[1]} ${mid},${end[1]} ${end[0]},${end[1]}`);
    path.setAttribute('fill','none');path.setAttribute('stroke','var(--accent)');path.setAttribute('stroke-width','1.5');path.setAttribute('marker-end','url(#map-arrow)');svg.append(path);
  }
  for(const item of $('map-before').querySelectorAll('.map-relation')) {
    const r=item.getBoundingClientRect(); wire([r.right-graph.left,r.top+r.height/2-graph.top],[center.left-graph.left-4,center.top+center.height/2-graph.top]);
  }
  for(const item of $('map-after').querySelectorAll('.map-relation')) {
    const r=item.getBoundingClientRect();wire([center.right-graph.left,center.top+center.height/2-graph.top],[r.left-graph.left-4,r.top+r.height/2-graph.top]);
  }
}
function selectNode(id) {
  if(!nodes.has(id)) return;
  selected=id;const node=nodes.get(id);
  $('map-focus-title').textContent='正在连接：'+node.title;
  const before=data.edges.filter(e=>e.kind==='learn' && e.target===id);
  const after=data.edges.filter(e=>e.kind==='learn' && e.source===id);
  $('map-before').replaceChildren(text('h5','① 建议先会'));
  $('map-after').replaceChildren(text('h5','③ 可以用到'));
  for(const rel of before) $('map-before').append(relationBox(rel,rel.source));
  for(const rel of after) $('map-after').append(relationBox(rel,rel.target));
  if(!before.length) $('map-before').append(text('p','从这里开始，先跑通第一个程序。','muted'));
  if(!after.length) $('map-after').append(text('p','进入第二阶段前，先完成本课程项目验收。','muted'));
  const center=text('div','','map-selected');center.append(text('small',`② 当前知识 · 第 ${String(node.chapter).padStart(2,'0')} 章`),text('strong',node.title),text('p',node.idea));
  $('map-current').replaceChildren(center);
  const detail=$('map-detail');detail.replaceChildren();
  const memory=text('p',node.memory,'map-memory');memory.prepend(text('b','一句话记忆：'));detail.append(memory);
  const pitfall=text('p',node.pitfall);pitfall.prepend(text('b','别混在一起：'));detail.append(pitfall);
  const related=text('div','','map-associations');related.append(text('h5','联想对照 · 虚线不表示先修要求'));
  const connections=data.edges.filter(e=>e.kind==='connect' && (e.source===id || e.target===id));
  for(const rel of connections) related.append(relationBox(rel,rel.source===id?rel.target:rel.source));
  if(!connections.length) related.append(text('p','试着用上面的学习联系解释：当前知识为什么会在下一个场景用到？'));
  detail.append(related);
  const question=text('p',node.question);question.prepend(text('b','合上答案，先说一遍：'));detail.append(question);
  const answer=document.createElement('details');answer.append(text('summary','展开自测解析'),text('p',node.answer));detail.append(answer);
  const actions=text('p','','map-reading-links');
  const chapter=text('a','阅读对应章节 →');chapter.href='#'+node.target;
  const example=text('a',node.id==='project'?'打开成绩项目 →':node.id==='next'?'查看后续路线 →':'运行关联示例 →');example.href='#'+node.example;
  actions.append(chapter,example);detail.append(actions);
  for(const link of document.querySelectorAll('[data-map-node]')) {
    if(link.dataset.mapNode===id) link.setAttribute('aria-current','true');else link.removeAttribute('aria-current');
  }
  requestAnimationFrame(redraw);
}
function selectRoute(id) {
  const route=data.routes.find(r=>r.id===id);if(!route)return;
  for(const button of root.querySelectorAll('[data-map-route]')) button.setAttribute('aria-pressed',String(button.dataset.mapRoute===id));
  const out=$('map-route-detail');out.replaceChildren(text('p',route.goal));
  const chain=text('ol','','map-chain');
  for(const [i,key] of route.nodes.entries()) { const li=document.createElement('li');li.append(text('span',String(i+1).padStart(2,'0')),nodeLink(key));chain.append(li); }
  out.append(chain,text('p','这条路线列出重点顺序；点击节点查看需要补学的知识。查看一条路线不代表已经完成它。','muted'));
  selectNode(route.nodes[0]);
}
function fromHash(scroll=false) {
  const match=/^#c00-map-([a-z]+)$/.exec(location.hash);
  if(match && nodes.has(match[1])) {
    selectNode(match[1]);
    if(scroll) requestAnimationFrame(()=>{ $('map-focus').scrollIntoView({block:'start'}); $('map-focus').focus({preventScroll:true}); });
  } else requestAnimationFrame(redraw);
}
for(const button of root.querySelectorAll('[data-map-route]')) button.addEventListener('click',()=>{
  selectRoute(button.dataset.mapRoute);
  // Keep URL and visible selection consistent without adding a route to progress data.
  history.replaceState(null,'','#c00-map-'+selected);
});
document.addEventListener('click',event=>{
  const link=event.target.closest('a[data-map-node]');if(!link)return;
  if(location.hash===link.hash) fromHash(true);
});
window.addEventListener('hashchange',()=>fromHash(true));
$('map-search').addEventListener('input',()=>{
  const q=$('map-search').value.trim().toLocaleLowerCase();let count=0;
  for(const link of root.querySelectorAll('.map-catalog [data-map-node]')) {
    const node=nodes.get(link.dataset.mapNode);
    const corpus=[node.title,node.idea,node.memory,node.question,node.answer,node.pitfall,...data.edges.filter(e=>e.source===node.id||e.target===node.id).map(e=>e.why)].join(' ').toLocaleLowerCase();
    link.hidden=!!q&&!corpus.includes(q);if(!link.hidden)count++;
  }
  for(const group of root.querySelectorAll('.map-catalog section')) group.hidden=![...group.querySelectorAll('[data-map-node]')].some(a=>!a.hidden);
  $('map-search-status').textContent=count?`找到 ${count} 个知识点`:'没有匹配项。试试“返回”“字符串”或清空搜索。';
});
selectRoute('start');fromHash(true);
new ResizeObserver(()=>requestAnimationFrame(redraw)).observe($('map-graph'));
window.addEventListener('beforeprint',redraw);
window.addEventListener('afterprint',()=>requestAnimationFrame(redraw));
})();
