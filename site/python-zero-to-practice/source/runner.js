// 在网页上运行示例、核对练习：点击后才加载浏览器中的 Python（Pyodide），离线学习包仍以本机 Python 为准。
(() => {
'use strict';
const $ = selector => document.querySelector(selector);
const all = selector => [...document.querySelectorAll(selector)];
const DATA = JSON.parse($('#run-data').textContent);
const LIMIT = 5000;   // 与 tools/check_practice.py 相同的单次运行上限
const BOOT_LIMIT = 120000;
const CODE_KEY = 'python-zero-practice-v1:code:';
let worker = null, busy = false, booted = false;

const store = {
  get(key) { try { return localStorage.getItem(key); } catch (_) { return null; } },
  set(key, value) { try { localStorage.setItem(key, value); } catch (_) { /* 浏览器不允许保存时，本次仍可运行 */ } },
  remove(key) { try { localStorage.removeItem(key); } catch (_) { /* 同上 */ } },
};
const normalize = text => text.replace(/\r\n/g, '\n').replace(/\n+$/, '');

function makeWorker() {
  const source = new Blob([$('#py-worker').textContent], { type: 'text/javascript' });
  return new Worker(URL.createObjectURL(source));
}

// 一次只运行一段代码；超时就结束 Worker，下一次运行会重新加载。
function run(job, onBoot) {
  return new Promise(resolve => {
    try { worker = worker || makeWorker(); } catch (_) { resolve({ type: 'failed', message: 'worker' }); return; }
    let timer = setTimeout(() => finish({ type: 'timeout', stage: booted ? 'run' : 'boot' }), booted ? LIMIT : BOOT_LIMIT);
    const finish = result => {
      clearTimeout(timer);
      worker.onmessage = worker.onerror = null;
      if (result.type === 'timeout' || result.type === 'failed') { worker.terminate(); worker = null; booted = false; }
      resolve(result);
    };
    worker.onmessage = ({ data }) => {
      if (data.type === 'ready') {
        if (!booted) { booted = true; onBoot(); clearTimeout(timer); timer = setTimeout(() => finish({ type: 'timeout', stage: 'run' }), LIMIT); }
        return;
      }
      finish(data);
    };
    worker.onerror = event => { event.preventDefault(); finish({ type: 'failed', message: event.message || 'worker' }); };
    worker.postMessage(job);
  });
}

function firstDifference(expected, actual) {
  const a = normalize(expected).split('\n'), b = normalize(actual).split('\n');
  for (let i = 0; i < Math.max(a.length, b.length); i++) {
    if (a[i] !== b[i]) return { line: i + 1, expected: a[i] === undefined ? '<没有这一行>' : JSON.stringify(a[i]), actual: b[i] === undefined ? '<没有这一行>' : JSON.stringify(b[i]) };
  }
  return null;
}

function panelFor(anchor) {
  let panel = anchor.nextElementSibling;
  if (!panel || !panel.classList.contains('run-output')) {
    panel = document.createElement('div');
    panel.className = 'run-output';
    panel.setAttribute('role', 'status');
    anchor.after(panel);
  }
  return panel;
}

function show(panel, verdict, kind, result, extra = '') {
  panel.replaceChildren();
  panel.dataset.kind = kind;
  const head = document.createElement('p');
  head.className = 'run-verdict';
  head.textContent = verdict;
  panel.append(head);
  if (extra) { const p = document.createElement('p'); p.className = 'run-note'; p.textContent = extra; panel.append(p); }
  for (const [label, text] of [['程序输出', result && result.stdout], ['错误信息', result && result.stderr]]) {
    if (!text) continue;
    const title = document.createElement('h5'); title.textContent = label;
    const pre = document.createElement('pre'); pre.textContent = text;
    panel.append(title, pre);
  }
}

function explain(result, item, path) {
  if (result.type === 'timeout' && result.stage === 'boot') return ['加载太久', 'error', '浏览器中的 Python 约 10 MB，网络较慢时可能超过两分钟。请稍后再试，或用本机 Python 运行：python ' + path];
  if (result.type === 'timeout') return ['超过 5 秒', 'error', '检查是否出现无限循环，或多读了一次 input。运行环境已重启，下次点击会重新加载。'];
  if (result.type === 'failed') return ['没能启动浏览器中的 Python', 'error', '需要联网下载 Pyodide；离线学习包或受限网络里请用本机 Python 运行：python ' + path];
  if (result.status === 'error') {
    const more = /EOFError/.test(result.stderr) ? '程序还想读取输入，但输入已经用完：本题提供的输入见上方。' : '先看错误信息最后一行，再找“你的代码.py”后面的行号。';
    return ['运行报错', 'error', more];
  }
  if (result.status === 'tests') return ['额外测试未通过', 'error', '输出可能正确，但函数在其他输入下不对。看错误信息里的 assert：它写出了这次的输入和期望结果。'];
  const diff = firstDifference(item.output, result.stdout);
  if (diff) return ['输出不同', 'diff', `第 ${diff.line} 行不同（引号帮助看清空格）：预期 ${diff.expected}，实际 ${diff.actual}。请检查空格、大小写和多余的提示文字。`];
  return null;
}

async function execute(button, job, item, path, panel, success) {
  if (busy) { show(panel, '上一段代码还在运行', 'info', null, '请等它结束再试。'); return; }
  busy = true;
  const label = button.textContent;
  button.disabled = true;
  button.textContent = booted ? '运行中…' : '正在加载 Python…';
  if (!booted) show(panel, '正在加载浏览器中的 Python', 'info', null, '只在第一次运行时下载，约 10 MB。之后每次运行几乎立即开始。');
  const result = await run(job, () => { button.textContent = '运行中…'; });
  const problem = explain(result, item, path);
  if (problem) show(panel, problem[0], problem[1], result, problem[2]);
  else show(panel, success[0], 'pass', result, success[1]);
  button.textContent = label;
  button.disabled = false;
  busy = false;
}

// 示例：运行教材里的代码，并与预期输出对照
all('button[data-run-example]').forEach(button => button.addEventListener('click', () => {
  const id = button.dataset.runExample, item = DATA.examples[id];
  const box = button.closest('.codebox');
  execute(button, { code: box.querySelector('pre code').textContent + '\n', stdin: item.stdin, tests: '' }, item,
    'examples/ch' + id.slice(0, 2) + '/ex' + id + '.py', panelFor(box),
    ['与预期输出一致', '试试“动手改写”：复制代码到自己的 .py 文件里改，再预测结果。']);
}));

// 练习：在网页上作答，用与自检器相同的输入、预期输出和额外断言核对
all('.try-here').forEach(box => {
  const id = box.dataset.exercise, item = DATA.exercises[id];
  const editor = box.querySelector('textarea');
  const key = CODE_KEY + id;
  let loaded = false;
  box.addEventListener('toggle', () => {
    if (!box.open || loaded) return;
    loaded = true;
    editor.value = store.get(key) ?? item.starter;
  });
  let saving;
  editor.addEventListener('input', () => { clearTimeout(saving); saving = setTimeout(() => store.set(key, editor.value), 300); });
  // Tab 缩进四个空格；按 Esc 之后的下一个 Tab 离开编辑框
  let leaving = false;
  editor.addEventListener('keydown', event => {
    if (event.key === 'Escape') { leaving = true; return; }
    if (event.key !== 'Tab' || event.shiftKey || leaving) { leaving = false; return; }
    event.preventDefault();
    editor.setRangeText('    ', editor.selectionStart, editor.selectionEnd, 'end');
    editor.dispatchEvent(new Event('input'));
  });
  box.querySelector('[data-reset]').addEventListener('click', () => {
    if (editor.value !== item.starter && !window.confirm('恢复起始代码会清除这里的作答，确定吗？')) return;
    editor.value = item.starter; store.remove(key);
  });
  const button = box.querySelector('[data-run-exercise]');
  button.addEventListener('click', () => execute(button, { code: editor.value, stdin: item.stdin, tests: item.tests }, item, item.path,
    panelFor(box.querySelector('.run-actions')),
    [item.tests ? '通过：输出一致，额外测试也通过' : '通过：输出与预期一致', '如果是你独立完成的，可以勾选上方的“我已独立完成”。也建议把代码保存进 ' + item.path + '。']));
});
})();
