(() => {
'use strict';
const $ = selector => document.querySelector(selector);
const all = selector => [...document.querySelectorAll(selector)];
const COURSE = 'python-zero-practice-v1';
const KEY = COURSE + ':progress';
const allowed = new Set(all('[data-check]').map(el => el.dataset.check));
const noteKeys = new Set(all('[data-note]').map(el => el.dataset.note));
const blank = () => ({course: COURSE, version: 1, checks: {}, notes: {}, chapter: 'c00', theme: 'light'});
let state = blank();
let statusTimer;
function say(message) { $('#status').textContent = message; clearTimeout(statusTimer); statusTimer = setTimeout(() => { $('#status').textContent = ''; }, 6000); }
function validate(raw) {
  if (!raw || raw.course !== COURSE || raw.version !== 1 || !raw.checks || typeof raw.checks !== 'object' || !raw.notes || typeof raw.notes !== 'object') throw new Error('这不是本教材 v1 的进度文件。');
  const clean = blank();
  for (const key of allowed) if (raw.checks[key] === true) clean.checks[key] = true;
  for (const key of noteKeys) if (typeof raw.notes[key] === 'string') clean.notes[key] = raw.notes[key].slice(0,20000);
  if (/^c(0\d|1[0-8])$/.test(raw.chapter || '')) clean.chapter = raw.chapter;
  if (raw.theme === 'dark') clean.theme = 'dark';
  return clean;
}
try { const saved = localStorage.getItem(KEY); if (saved) state = validate(JSON.parse(saved)); } catch (_) { $('#storage-warning').hidden = false; }
function save() { try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (_) { $('#storage-warning').hidden = false; } }
function renderState() {
  document.documentElement.dataset.theme = state.theme;
  all('[data-check]').forEach(el => { el.checked = state.checks[el.dataset.check] === true; });
  all('[data-note]').forEach(el => { el.value = state.notes[el.dataset.note] || ''; });
  progress();
}
function progress() {
  let chapters = 0, exercises = 0;
  for (const key of allowed) if (state.checks[key]) { if (key.startsWith('chapter:')) chapters++; else exercises++; }
  $('#progress').value = chapters;
  $('#progress-label').textContent = `已完成 ${chapters} / 19 章`;
  $('#exercise-progress').textContent = `独立完成 ${exercises} / 100 题`;
  all('[data-nav]').forEach(el => { const done = state.checks['chapter:' + el.dataset.nav]; el.querySelector('.nav-done').textContent = done ? '✓' : ''; });
}
function route(scroll = true) {
  let hash; try { hash = decodeURIComponent(location.hash.slice(1)); } catch (_) { hash='c00'; }
  const id = /^c(?:0\d|1[0-8])/.exec(hash)?.[0] || state.chapter;
  const active = document.getElementById(id) || $('#c00');
  all('.chapter').forEach(el => { el.hidden = el !== active; });
  all('[data-nav]').forEach(el => { if ('c' + el.dataset.nav === active.id) el.setAttribute('aria-current','page'); else el.removeAttribute('aria-current'); });
  state.chapter = active.id;
  $('#breadcrumb').textContent = active.id.slice(1) + ' / ' + active.querySelector('.chapter-header h2').textContent;
  document.body.classList.remove('nav-open'); $('#toggle-nav').setAttribute('aria-expanded','false');
  save();
  if (scroll) requestAnimationFrame(() => { const target = document.getElementById(hash); if (target && target !== active && active.contains(target)) target.scrollIntoView({block:'start'}); else window.scrollTo(0,0); });
}
all('[data-check]').forEach(el => el.addEventListener('change', () => { state.checks[el.dataset.check] = el.checked; save(); progress(); }));
all('[data-note]').forEach(el => el.addEventListener('input', () => { state.notes[el.dataset.note] = el.value; save(); }));
window.addEventListener('hashchange', () => route());
$('#toggle-nav').addEventListener('click', () => { const open = document.body.classList.toggle('nav-open'); $('#toggle-nav').setAttribute('aria-expanded', String(open)); });
$('#theme').addEventListener('click', () => { state.theme = state.theme === 'dark' ? 'light' : 'dark'; document.documentElement.dataset.theme = state.theme; save(); });
$('#export-progress').addEventListener('click', () => {
  const file = new Blob([JSON.stringify({...state, exportedAt: new Date().toISOString()}, null, 2)], {type:'application/json;charset=utf-8'});
  const url = URL.createObjectURL(file); const link = document.createElement('a'); link.href = url; link.download = 'python-learning-progress.json'; document.body.append(link); link.click(); link.remove(); setTimeout(() => URL.revokeObjectURL(url), 10000);
  say('进度已导出。请同时复制 practice、projects 和 notes 中的文件。');
});
$('#import-progress').addEventListener('click', () => { $('#import-file').value = ''; $('#import-file').click(); });
$('#import-file').addEventListener('change', async event => {
  const file = event.target.files[0]; if (!file) return;
  try {
    if (file.size > 2000000) throw new Error('进度文件过大，请选择本教材导出的 JSON。');
    const imported = validate(JSON.parse(await file.text()));
    if (!window.confirm('导入会替换本浏览器当前的章节勾选与笔记。尚未备份时请取消，先导出。继续导入？')) return;
    state = imported; renderState(); save();
    location.hash = state.chapter; route(); say('已导入进度和笔记；你的 .py 文件需要另行复制。');
  } catch (error) { say('导入失败：' + error.message); }
});
const searchData = JSON.parse($('#search-data').textContent);
$('#search').addEventListener('input', event => {
  const query = event.target.value.trim().toLocaleLowerCase();
  $('#chapter-nav').hidden = !!query; $('#search-results').hidden = !query; $('#search-results').replaceChildren();
  if (!query) return;
  const matches = searchData.filter(item => (item.title + ' ' + item.text).toLocaleLowerCase().includes(query));
  const count = document.createElement('p'); count.textContent = `找到 ${matches.length} 项${matches.length>40?'，先显示前 40 项':''}`; $('#search-results').append(count);
  for (const item of matches.slice(0,40)) { const link = document.createElement('a'); link.href = '#' + item.target; const kind = document.createElement('small'); kind.textContent = item.kind; const title = document.createElement('span'); title.textContent = item.title; link.append(kind,title); link.addEventListener('click', () => { if (location.hash === link.hash) route(); }); $('#search-results').append(link); }
});
all('.copy').forEach(button => button.addEventListener('click', async () => {
  const code = button.closest('.codebox').querySelector('pre code').textContent;
  let copied = false;
  try { await navigator.clipboard.writeText(code); copied = true; } catch (_) {
    const input = document.createElement('textarea'); input.value = code; input.style.position='fixed'; input.style.left='-9999px'; document.body.append(input); input.select(); try { copied = document.execCommand('copy'); } catch (_) {} input.remove();
  }
  if (copied) { const old = button.textContent; button.textContent='已复制'; setTimeout(() => {button.textContent=old;},1700); }
  else { const selection = window.getSelection(); const range = document.createRange(); range.selectNodeContents(button.closest('.codebox').querySelector('pre code')); selection.removeAllRanges(); selection.addRange(range); say('浏览器未允许自动复制，代码已选中，请按 Ctrl+C 或 Command+C。'); }
}));
let printDetails = [];
window.addEventListener('beforeprint', () => { printDetails = all('.chapter:not([hidden]) details').map(el => [el, el.open]); printDetails.forEach(([el]) => {el.open=true;}); });
window.addEventListener('afterprint', () => { printDetails.forEach(([el, wasOpen]) => {el.open=wasOpen;}); });
$('#print').addEventListener('click', () => window.print());
const e = text => String(text).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
all('[data-lab]').forEach(lab => {
  let step=0;
  const kind = lab.dataset.lab;
  const render = () => {
    let content, maximum;
    if (kind==='loop') {
      const frames=[['初始化','—',0,'total = 0；循环尚未开始。'],['第 1 轮',2,2,'取到 2，旧 total=0；0+2 得到 2。'],['第 2 轮',4,6,'取到 4，旧 total=2；2+4 得到 6。'],['第 3 轮',1,7,'取到 1，旧 total=6；6+1 得到 7。'],['循环结束','—',7,'已经取完全部元素，退出循环，最终总和 7。']];
      maximum=frames.length-1; const f=frames[step]; content=`<strong>${f[0]}</strong><div class="state-row"><div class="state-cell"><small>本轮 value</small><b>${f[1]}</b></div><div class="state-cell"><small>累计 total</small><b>${f[2]}</b></div></div><p>${f[3]}</p>`;
    } else if (kind==='alias') {
      maximum=3; const copy=lab.querySelector('.alias-mode').value==='copy';
      const shared = !copy; const a=step>=2 && shared ? '[1, 2, 3]' : '[1, 2]'; const b=step===3 ? '[9]' : step>=2 ? '[1, 2, 3]' : '[1, 2]';
      const captions=['执行 a = [1, 2]，建立第一个列表。',copy?'执行 b = a.copy()，新建外层列表 B。':'执行 b = a，两个名字指向同一个列表 A。','执行 b.append(3)，修改 b 指向的对象。','执行 b = [9]，仅把名字 b 改绑到新列表 C。'];
      content=`<strong>步骤 ${step+1} / 4</strong><div class="object-row"><code>a</code><span>→</span><code>列表 A ${e(a)}</code></div>`;
      if(step>0) content+=`<div class="object-row"><code>b</code><span>→</span><code>列表 ${step===3?'C':copy?'B':'A'} ${e(b)}</code></div>`;
      content+=`<p>${captions[step]}</p>`;
    } else {
      const frames=[['定义函数','def add(a, b): return a + b','此时函数体尚未被这次调用执行。'],['调用与绑定','a = 2    b = 3','调用 add(2, 3)，给本次函数执行绑定参数。'],['计算表达式','a + b → 5','读取局部参数，进行加法。'],['返回给调用处','return 5','当前函数结束，把 5 交回调用表达式。'],['保存结果','answer = 5','调用表达式 add(2,3) 的结果交给 answer，外层程序继续。']];
      maximum=frames.length-1; const f=frames[step]; content=`<strong>${f[0]}</strong><div class="state-row"><code>${e(f[1])}</code></div><p>${f[2]}</p>`;
    }
    lab.querySelector('.lab-screen').innerHTML=content;
    lab.querySelector('[data-step="-1"]').disabled=step===0;
    lab.querySelector('[data-step="1"]').disabled=step===maximum;
  };
  lab.querySelectorAll('[data-step]').forEach(button => button.addEventListener('click',()=>{step+=Number(button.dataset.step);render();}));
  lab.querySelector('[data-reset]').addEventListener('click',()=>{step=0;render();});
  lab.querySelector('select')?.addEventListener('change',()=>{step=0;render();});
  render();
});
renderState(); route(!!location.hash);
})();
