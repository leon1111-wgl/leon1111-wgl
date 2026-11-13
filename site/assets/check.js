/* Reading pages: one quick check in the middle of each chapter, marked at once.
   learn/data/checks-<course>.json (scripts/build_study.py) gives each chapter one of four kinds:
     mcq      choose; a wrong choice shows a hint (why that choice is wrong) and you try again
     numeric  type a number; a wrong one shows the first step of the solution as a hint
     predict  before unfolding a program's output, type what you think it prints; wrong lines are pointed out
     recall   answer one of the chapter's questions in your head, see the answer, say whether you had it
   The full answer shows after a right answer, a second wrong one, or "Show the answer". A miss joins the review queue
   (the same queue as the hub's practice), so it comes back on a later day. Nothing leaves the browser. */
(() => {
  const courseId = document.body.dataset.courseId;
  const articles = [...document.querySelectorAll('article.topic[id]')];
  const script = document.querySelector('script[src*="check.js"]');
  if (!courseId || !articles.length || !script) return;
  const zh = document.documentElement.lang.startsWith('zh');
  const L = (o) => (o && typeof o === 'object' && !Array.isArray(o) ? (o[zh ? 'zh' : 'en'] ?? o.en ?? o.zh) : o);
  const T = zh ? {
    head: '停一下，检查一下', mcq: '选一个答案', numeric: '算一算', predict: '先预测，再展开输出', recall: '先在心里回答，再看答案',
    check: '检查', show: '直接看答案', right: '答对了。', wrong: '再想想。', hint: '提示：', answer: '答案：', solution: '讲解',
    predictAsk: '上面这段程序会打印什么？在下面写出每一行，然后点“检查”。', predictWrong: (n, k) => `第 ${n} 行不对${k ? `（一共 ${k} 行不对）` : ''}。`,
    predictLines: (a, b) => `你写了 ${a} 行，程序打印 ${b} 行。`, firstStep: '程序的第一步：',
    had: '我答出来了', notYet: '还没答出来', queued: '已加入复习队列，过几天会再问你。', again: '读完这一章后再回来试一次。', kept: '好。', number: '你的答案', tolerance: (x) => `允许误差 ±${x}`,
  } : {
    head: 'Quick check', mcq: 'Choose one', numeric: 'Work it out', predict: 'Predict, then unfold the output', recall: 'Answer in your head, then look',
    check: 'Check', show: 'Show the answer', right: 'Right.', wrong: 'Not quite.', hint: 'Hint: ', answer: 'Answer: ', solution: 'Solution',
    predictAsk: 'What does the program above print? Write each line below, then press Check.', predictWrong: (n, k) => `Line ${n} is not right${k > 1 ? ` (${k} lines differ)` : ''}.`,
    predictLines: (a, b) => `You wrote ${a} lines; the program prints ${b}.`, firstStep: 'The program first: ',
    had: 'I had it', notYet: 'Not yet', queued: 'Added to your review queue; it will come back in a few days.', again: 'Come back to it after reading the rest of the chapter.', kept: 'Good.', number: 'Your answer', tolerance: (x) => `within ±${x}`,
  };
  const el = (tag, cls, text) => { const e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; };
  /* `code` and **bold** in question text, as on the hub */
  const rich = (text) => {
    const frag = document.createDocumentFragment();
    String(text ?? '').split('\n\n').forEach((para) => {
      const p = el('p');
      para.split(/(`[^`\n]+`|\*\*[^*\n]+\*\*)/).forEach((part) => {
        if (/^`[^`]+`$/.test(part)) p.append(el('code', null, part.slice(1, -1)));
        else if (/^\*\*[^*]+\*\*$/.test(part)) p.append(el('b', null, part.slice(2, -2)));
        else part.split('\n').forEach((line, i) => { if (i) p.append(document.createElement('br')); p.append(line); });
      });
      frag.append(p);
    });
    return frag;
  };
  const queue = (key) => {
    try {
      const saved = JSON.parse(localStorage.getItem('leon-learn-srs') || '{}');
      if (!(key in saved)) saved[key] = { fresh: true, added: Date.now() };
      localStorage.setItem('leon-learn-srs', JSON.stringify(saved));
    } catch (_) { /* private mode: the check still works for this visit */ }
  };
  const norm = (s) => s.replace(/\s+$/, '');

  function build(article, q, n) {
    const box = el('section', 'quick-check');
    box.dataset.qcKind = q.kind;
    box.dataset.qcState = 'open';
    const headId = `qc-${article.id}`;
    box.setAttribute('aria-labelledby', headId);
    const head = el('h3', null, `${T.head} · ${T[q.kind]}`);
    head.id = headId;
    box.append(head);
    if (q.title && q.kind !== 'predict' && q.kind !== 'recall') box.append(el('p', 'qc-title', L(q.title)));
    if (q.prompt) box.append(rich(L(q.prompt)));
    if (q.kind === 'recall') box.append(rich(L(q.q)));
    if (q.kind === 'predict') box.append(el('p', null, T.predictAsk));
    if (q.code) box.append(el('pre', 'code', q.code));
    const feedback = el('div', 'qc-feedback');
    feedback.dataset.qcFeedback = '';
    feedback.setAttribute('aria-live', 'polite');
    const solution = el('div', 'qc-solution');
    solution.dataset.qcSolution = '';
    solution.hidden = true;
    const actions = el('div', 'qc-actions');
    const reveal = el('button', 'qc-show', T.show);
    reveal.type = 'button';
    reveal.dataset.qcReveal = '';
    let misses = 0;
    const missed = () => { misses += 1; if (misses === 1 && q.queue !== false) queue(q.kind === 'recall' ? `${courseId}/${q.id}` : `q:${courseId}/${q.id}`); };
    const finish = (lead) => {
      box.dataset.qcState = 'done';
      solution.hidden = false;
      reveal.hidden = true;
      if (lead) { feedback.textContent = ''; feedback.append(el('p', 'qc-right', lead)); }
      box.querySelectorAll('input, textarea, [data-qc-check]').forEach((x) => { x.disabled = true; });
    };
    const say = (cls, text, hint) => {
      feedback.textContent = '';
      const p = el('p', cls, text);
      if (hint) { p.append(' '); p.append(el('b', null, T.hint)); p.append(...rich(hint).firstChild.childNodes); }
      feedback.append(p);
    };

    if (q.kind === 'mcq') {
      const list = el('div', 'qc-options');
      list.setAttribute('role', 'group');
      list.setAttribute('aria-label', T.mcq);
      q.options.forEach((o) => {
        const b = el('button', 'qc-option');
        b.type = 'button';
        b.dataset.qcOption = '';
        b.dataset.qcRight = o.right ? '1' : '0';
        b.append(...rich(L(o.text)).firstChild.childNodes);
        b.addEventListener('click', () => {
          if (box.dataset.qcState === 'done') return;
          if (o.right) {
            b.classList.add('is-right');
            b.setAttribute('aria-pressed', 'true');
            finish(T.right);
            list.querySelectorAll('button').forEach((x) => { x.disabled = true; });
            return;
          }
          b.classList.add('is-wrong');
          b.disabled = true;
          missed();
          if (misses >= 2) {
            finish(T.wrong);
            list.querySelectorAll('[data-qc-right="1"]').forEach((x) => x.classList.add('is-right'));
            list.querySelectorAll('button').forEach((x) => { x.disabled = true; });
          } else say('qc-wrong', T.wrong, L(o.why));
        });
        list.append(b);
      });
      box.append(list);
      const right = q.options.find((o) => o.right);
      solution.append(el('h4', null, T.solution));
      if (right?.why) solution.append(rich(L(right.why)));
      if (q.solution) solution.append(rich(L(q.solution)));
    }

    if (q.kind === 'numeric') {
      const row = el('div', 'qc-numeric');
      const input = el('input');
      input.type = 'text';
      input.inputMode = 'decimal';
      input.setAttribute('aria-label', T.number);
      const go = el('button', 'qc-check', T.check);
      go.type = 'button';
      go.dataset.qcCheck = '';
      row.append(input);
      if (q.unit) row.append(el('span', 'qc-unit', L(q.unit)));
      row.append(go);
      if (q.tolerance) row.append(el('small', 'qc-tol', T.tolerance(q.tolerance)));
      box.append(row);
      const steps = String(L(q.solution) || '').split(/\n+/).filter((x) => x.trim());
      const check = () => {
        const value = Number(input.value.trim().replace(/,/g, '').replace(/^(-?\d+)\/(\d+)$/, (_, a, b) => String(Number(a) / Number(b))));
        if (!input.value.trim()) return;
        if (Number.isFinite(value) && Math.abs(value - q.answer) <= (q.tolerance || 0) + 1e-9) { finish(`${T.right} ${T.answer}${q.answer}`); return; }
        missed();
        if (misses >= 2) finish(`${T.wrong} ${T.answer}${q.answer}`);
        else say('qc-wrong', T.wrong, steps[0] || '');
      };
      go.addEventListener('click', check);
      input.addEventListener('keydown', (e) => { if (e.key === 'Enter') check(); });
      solution.append(el('h4', null, T.solution), rich(L(q.solution)));
    }

    if (q.kind === 'predict') {
      const area = el('textarea', 'qc-answer');
      area.rows = Math.min(8, q.output.split('\n').length + 1);
      area.spellcheck = false;
      area.setAttribute('autocapitalize', 'off');
      area.setAttribute('aria-label', T.predict);
      const go = el('button', 'qc-check', T.check);
      go.type = 'button';
      go.dataset.qcCheck = '';
      box.append(area);
      actions.append(go);
      const want = q.output.replace(/\n$/, '').split('\n');
      const walk = L(q.walk) || [];
      go.addEventListener('click', () => {
        const got = area.value.replace(/\n+$/, '').split('\n');
        const bad = want.map((line, i) => norm(got[i] ?? '') === norm(line) ? -1 : i).filter((i) => i >= 0);
        if (!bad.length && got.length === want.length) { finish(T.right); return; }
        missed();
        if (misses >= 2) { finish(T.wrong); return; }
        const text = bad.length ? T.predictWrong(bad[0] + 1, bad.length) : T.predictLines(got.length, want.length);
        say('qc-wrong', text, walk[0] ? `${T.firstStep}${walk[0]}` : '');
      });
      solution.append(el('h4', null, T.answer), el('pre', 'code', q.output));
    }

    if (q.kind === 'recall') {
      reveal.textContent = T.show;
      solution.append(el('h4', null, T.answer), rich(L(q.a)));
      const had = el('div', 'qc-self');
      const yes = el('button', 'qc-check', T.had);
      const no = el('button', 'qc-check', T.notYet);
      yes.type = 'button'; no.type = 'button';
      yes.addEventListener('click', () => { had.remove(); say('qc-right', T.kept); });
      no.addEventListener('click', () => { missed(); had.remove(); say('qc-wrong', q.queue === false ? T.again : T.queued); });
      had.append(yes, no);
      solution.append(had);
    }

    reveal.addEventListener('click', () => {
      if (q.kind !== 'recall') missed();
      finish(q.kind === 'recall' ? '' : (q.kind === 'numeric' ? `${T.answer}${q.answer}` : ''));
    });
    actions.append(reveal);
    box.append(actions, feedback, solution);
    return box;
  }

  /* mid-chapter: a predict check goes inside its program, before the folded output; the others after the first
     worked problem or program, else after the guided questions */
  function place(article, box, q) {
    if (q.kind === 'predict') {
      const section = document.getElementById(q.anchor);
      const fold = section?.querySelector(':scope > details.try-first');
      if (section && article.contains(section)) { (fold || section.lastElementChild).before(box); return true; }
      return false;
    }
    const after = article.querySelector('.worked-problem, .code-example') || article.querySelector('.guided, .guided-questions');
    if (after) { after.after(box); return true; }
    const end = article.querySelector('.instructor-notes, .topic-nav');
    if (end) { end.before(box); return true; }
    return false;
  }

  fetch(new URL(`../learn/data/checks-${courseId}.json`, script.src)).then((r) => (r.ok ? r.json() : {})).then((checks) => {
    articles.forEach((article, n) => {
      const q = checks[article.id];
      if (!q) return;
      const box = build(article, q, n);
      if (!place(article, box, q) && q.kind === 'predict') return;
    });
  }).catch(() => { /* without the file the chapter still reads as before */ });
})();
