/* Reading pages: a Run and an Edit button on every example verified to work in the browser. */
(() => {
  const sections = [...document.querySelectorAll('.code-example[data-run]')];
  if (!sections.length) return;
  // Java needs WebAssembly GC: where it is missing, say so instead of offering a button that fails after a download
  const javaOk = (() => { try { return WebAssembly.validate(new Uint8Array([0, 97, 115, 109, 1, 0, 0, 0, 1, 5, 1, 95, 1, 127, 0])); } catch (_) { return false; } })();
  const zh = document.documentElement.lang.startsWith('zh');
  const T = zh ? {
    run: '运行', again: '再运行一次', edit: '修改代码', reset: '还原', loading: { python: '正在下载 Python（约 10 MB，只需一次）…', c: '正在准备 C 编译器…', java: '正在下载 Java 编译器（约 7 MB，只需一次）…' },
    compiling: '正在编译…', running: '正在运行…', same: '输出与下方的预期结果一致', differs: '输出与预期结果不同。如果你改过代码，这是正常的', compile: '编译没有通过', error: '程序出错结束', timeout: '运行超过 8 秒，已停止。可能是死循环', unavailable: '这个运行环境没能加载。检查网络后再试，或者下载代码在自己电脑上运行', stdout: '这次的输出', empty: '（没有输出）', noBrowser: '这个浏览器不能在网页上运行这段代码。请更新浏览器，或者下载到自己电脑上运行。', caution: { python: '', c: '这里的 C 不会检查内存错误：越界和空指针常常不报错。这类问题要在自己电脑上用 -fsanitize=address 检查。', java: '这里的 Java 是精简版，并非完整 JDK。结果不一致时，以自己电脑上的 JDK 为准。' },
  } : {
    run: 'Run', again: 'Run again', edit: 'Edit code', reset: 'Reset', loading: { python: 'Downloading Python (about 10 MB, once only)…', c: 'Preparing the C compiler…', java: 'Downloading the Java compiler (about 7 MB, once only)…' },
    compiling: 'Compiling…', running: 'Running…', same: 'Output matches the expected result below', differs: 'Output differs from the expected result. That is normal if you changed the code', compile: 'It did not compile', error: 'The program stopped with an error', timeout: 'Stopped after 8 seconds. This may be an endless loop', unavailable: 'This runtime could not load. Check your connection and try again, or download the code and run it on your computer', stdout: 'This run printed', empty: '(no output)', noBrowser: 'This browser cannot run this code on the page. Update it, or download the code and run it on your computer.', caution: { python: '', c: 'C here does not check memory errors: out-of-bounds and null pointers often go unreported. Check those on your own machine with -fsanitize=address.', java: 'Java here is a reduced library, not a full JDK. If results disagree, trust a real JDK.' },
  };
  let module = null;
  const base = document.querySelector('script[src*="run-ui.js"]')?.src;
  const load = () => { module ??= import(new URL('runner/run.js', base).href); return module; };
  sections.forEach((section) => {
    const language = section.dataset.run;
    const code = section.querySelector('pre.code.highlighted code');
    const pre = code?.closest('pre');
    const actions = section.querySelector('.code-actions');
    if (!code || !actions) return;
    if (typeof WebAssembly !== 'object' || typeof Worker === 'undefined' || (language === 'java' && !javaOk)) {
      const note = Object.assign(document.createElement('p'), { className: 'run-machine', textContent: T.noBrowser });
      actions.after(note);
      return;
    }
    const source = code.textContent;
    const expected = section.querySelector('.code-output')?.textContent ?? '';
    const runButton = Object.assign(document.createElement('button'), { type: 'button', className: 'run-button', textContent: T.run });
    const editButton = Object.assign(document.createElement('button'), { type: 'button', textContent: T.edit });
    actions.insertBefore(editButton, actions.children[1]);
    actions.insertBefore(runButton, editButton);
    const panel = document.createElement('div');
    panel.className = 'run-panel';
    panel.hidden = true;
    panel.setAttribute('aria-live', 'polite');
    pre.after(panel);
    let editor = null;
    const current = () => (editor ? editor.value : source);
    const show = (statusClass, text, output) => {
      panel.hidden = false;
      panel.dataset.state = statusClass;
      panel.innerHTML = '';
      const line = document.createElement('p');
      line.className = 'run-status';
      line.textContent = text;
      panel.append(line);
      if (output !== undefined) {
        const box = document.createElement('pre');
        box.className = 'code';
        box.textContent = output || T.empty;
        panel.append(box);
      }
      const note = T.caution[language];
      if (note && statusClass !== 'busy') {
        const caution = document.createElement('p');
        caution.className = 'run-caution';
        caution.textContent = note;
        panel.append(caution);
      }
    };
    runButton.addEventListener('click', async () => {
      runButton.disabled = true;
      show('busy', T.loading[language]);
      try {
        const { run } = await load();
        const result = await run({ language, code: current(), onStatus: (stage) => show('busy', stage === 'compiling' ? T.compiling : T.running) });
        const same = result.stdout.replace(/\n$/, '') === expected.replace(/\n$/, '');
        const text = result.status === 'ok' ? (same ? T.same : T.differs) : (T[result.status] || T.error);
        const merged = [result.stdout, result.stderr].filter(Boolean).join(result.stdout.endsWith('\n') ? '' : '\n');
        show(result.status === 'ok' ? (same ? 'good' : 'plain') : 'bad', text, merged);
        // a beginner's first error message: say in plain words what it means and what to try, above the raw text
        if (result.status !== 'ok') {
          try {
            const { explainNode } = await import(new URL('runner/explain.js', base).href);
            const note = explainNode(result, { language, lang: zh ? 'zh' : 'en' });
            if (note) panel.querySelector('.run-status').after(note);
          } catch (_) { /* the raw message is still shown */ }
        }
        runButton.textContent = T.again;
      } catch (error) {
        show('bad', T.unavailable);
      }
      runButton.disabled = false;
    });
    editButton.addEventListener('click', () => {
      if (editor) {
        editor.remove();
        editor = null;
        pre.hidden = false;
        editButton.textContent = T.edit;
        return;
      }
      editor = document.createElement('textarea');
      editor.className = 'run-editor';
      editor.spellcheck = false;
      editor.autocapitalize = 'off';
      editor.setAttribute('autocorrect', 'off');
      editor.setAttribute('aria-label', T.edit);
      editor.value = source;
      editor.rows = Math.min(28, source.split('\n').length + 1);
      editor.addEventListener('keydown', (event) => {
        if (event.key === 'Tab' && !event.shiftKey) {
          event.preventDefault();
          editor.setRangeText('    ', editor.selectionStart, editor.selectionEnd, 'end');
        }
      });
      pre.hidden = true;
      pre.after(editor);
      editButton.textContent = T.reset;
      editor.focus();
    });
  });
})();
