/* Step-through diagrams inside chapters. Each <figure class="viz" data-viz="kind"> names a kind;
   the kind turns the chapter's own worked example into frames (a state plus one sentence), and one
   shared player steps through them. The numbers match the example printed above each figure. */
(() => {
  const zh = document.documentElement.lang.startsWith('zh');
  const tr = (z, e) => (zh ? z : e);
  const still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const NS = 'http://www.w3.org/2000/svg';
  const h = (tag, cls, html) => { const n = document.createElement(tag); if (cls) n.className = cls; if (html !== undefined) n.innerHTML = html; return n; };
  const s = (tag, attrs = {}, text) => { const n = document.createElementNS(NS, tag); Object.entries(attrs).forEach(([k, v]) => n.setAttribute(k, v)); if (text !== undefined) n.textContent = text; return n; };
  const fmt = (x, d = 2) => (Math.abs(x) < 5e-10 ? 0 : x).toFixed(d).replace('-', '−');
  const list = (a) => `[${a.join(', ')}]`;
  const ICON = {
    reset: '<path d="M4 12a8 8 0 1 0 2.4-5.7M4 4v4h4"/>',
    prev: '<path d="M15 6l-6 6 6 6"/>', next: '<path d="M9 6l6 6-6 6"/>',
    play: '<path d="M8 5.5v13l10-6.5z" fill="currentColor"/>', pause: '<path d="M8.5 5.5v13M15.5 5.5v13"/>',
  };
  const icon = (n) => `<svg viewBox="0 0 24 24" aria-hidden="true">${ICON[n]}</svg>`;
  const KINDS = {};

  /* ------------------------------------------------------------ the player */
  function mount(fig) {
    const kind = KINDS[fig.dataset.viz];
    const body = fig.querySelector('.viz-body');
    if (!kind || !body) return;
    const options = kind.options ? kind.options() : null;
    let choice = options ? options[0].value : null;
    let frames = []; let draw = () => {}; let at = 0; let timer = null;
    // a typed value that equals a preset presses that preset's chip
    const custom = kind.custom ? kind.custom((value) => { choice = value; opts.querySelectorAll('button').forEach((x) => x.setAttribute('aria-pressed', String(x.dataset.value === value))); build(); }) : null;

    const opts = h('div', 'viz-options');
    if (options) {
      opts.setAttribute('role', 'group');
      opts.setAttribute('aria-label', tr('选择示例', 'Choose an example'));
      options.forEach((o) => {
        const b = h('button', '', o.label);
        b.type = 'button';
        b.dataset.value = o.value;
        b.setAttribute('aria-pressed', String(o.value === choice));
        b.addEventListener('click', () => { choice = o.value; custom?.reset(); opts.querySelectorAll('button').forEach((x) => x.setAttribute('aria-pressed', String(x === b))); build(); });
        opts.append(b);
      });
      if (custom) opts.append(custom);
    }
    const stage = h('div', 'viz-stage');
    const bar = h('div', 'viz-bar');
    bar.innerHTML = `<div class="viz-controls">
      <button type="button" data-a="reset" aria-label="${tr('从头开始', 'Start over')}">${icon('reset')}</button>
      <button type="button" data-a="prev" aria-label="${tr('上一步', 'Previous step')}">${icon('prev')}</button>
      <button type="button" data-a="play" class="viz-play" aria-label="${tr('播放', 'Play')}">${icon('play')}</button>
      <button type="button" data-a="next" aria-label="${tr('下一步', 'Next step')}">${icon('next')}</button>
    </div><span class="viz-count"></span>`;
    const msg = h('p', 'viz-msg');
    msg.setAttribute('aria-live', 'polite');
    const progress = h('div', 'viz-progress', '<i></i>');
    body.append(...(options ? [opts] : []), stage, progress, msg, bar);
    const [reset, prev, play, next] = ['reset', 'prev', 'play', 'next'].map((a) => bar.querySelector(`[data-a="${a}"]`));
    const count = bar.querySelector('.viz-count');

    const stop = () => { clearInterval(timer); timer = null; play.innerHTML = icon('play'); play.setAttribute('aria-label', tr('播放', 'Play')); };
    const show = () => {
      draw(frames[at], at);
      msg.innerHTML = frames[at].msg;
      count.textContent = `${at + 1} / ${frames.length}`;
      progress.firstChild.style.width = `${frames.length > 1 ? (at / (frames.length - 1)) * 100 : 100}%`;
      const focused = document.activeElement;
      prev.disabled = at === 0;
      next.disabled = at === frames.length - 1;
      if ((focused === prev && prev.disabled) || (focused === next && next.disabled)) play.focus();
    };
    function build() {
      stop();
      const made = kind.build(choice);
      frames = made.frames;
      stage.innerHTML = '';
      stage.className = `viz-stage viz-${fig.dataset.viz}`;
      draw = made.mount(stage);
      at = 0;
      show();
    }
    reset.addEventListener('click', () => { stop(); at = 0; show(); });
    prev.addEventListener('click', () => { stop(); at = Math.max(0, at - 1); show(); });
    next.addEventListener('click', () => { stop(); at = Math.min(frames.length - 1, at + 1); show(); });
    play.addEventListener('click', () => {
      if (timer) { stop(); return; }
      if (at === frames.length - 1) at = 0;
      show();
      play.innerHTML = icon('pause');
      play.setAttribute('aria-label', tr('暂停', 'Pause'));
      timer = setInterval(() => { if (at >= frames.length - 1) { stop(); return; } at += 1; show(); }, still ? 2400 : 1500);
    });
    build();
  }

  /* ------------------------------------------------------------ COMP2123 · insertion and selection sort */
  KINDS.sort = {
    options: () => [{ value: 'insertion', label: tr('插入排序', 'Insertion sort') }, { value: 'selection', label: tr('选择排序', 'Selection sort') }],
    build(mode) {
      const a = [5, 2, 4, 1];
      const frames = [];
      const snap = (extra, text) => frames.push({ order: [...a], ...extra, msg: text });
      if (mode === 'insertion') {
        let shifts = 0;
        snap({ sorted: 1, count: 0 }, tr('已排好的前缀是 <b>[5]</b>，接下来把后面的数一个个插进去。', 'The sorted prefix is <b>[5]</b>. Insert the remaining values one at a time.'));
        for (let i = 1; i < a.length; i += 1) {
          const key = a[i];
          let j = i - 1;
          snap({ sorted: i, key, count: shifts }, tr(`取出 <b>${key}</b>，在前缀里给它找位置。`, `Lift out <b>${key}</b> and find its place in the prefix.`));
          while (j >= 0 && a[j] > key) {
            a[j + 1] = a[j];
            a[j] = key;
            shifts += 1;
            snap({ sorted: i, key, hot: [a[j + 1]], count: shifts }, tr(`${a[j + 1]} &gt; ${key}，把 ${a[j + 1]} 右移一格（第 ${shifts} 次移动）。`, `${a[j + 1]} &gt; ${key}, so shift ${a[j + 1]} one place right (shift ${shifts}).`));
            j -= 1;
          }
          snap({ sorted: i + 1, count: shifts, hot: [key] }, tr(`放下 ${key}，前缀变成 <b>${list(a.slice(0, i + 1))}</b>。`, `Drop ${key} in place. The prefix is now <b>${list(a.slice(0, i + 1))}</b>.`));
        }
        snap({ sorted: 4, count: shifts, done: true }, tr(`完成：<b>${list(a)}</b>。一共移动 ${shifts} 次，正好等于原数组里逆序对的个数。`, `Done: <b>${list(a)}</b>. ${shifts} shifts in total, exactly the number of inversions in the input.`));
      } else {
        let comps = 0;
        snap({ sorted: 0, count: 0 }, tr('每一轮在没排好的部分里找最小值，放到前面。', 'Each pass finds the smallest value in the unsorted part and moves it to the front.'));
        for (let i = 0; i < a.length - 1; i += 1) {
          let m = i;
          snap({ sorted: i, min: a[m], count: comps }, tr(`第 ${i + 1} 轮：先把 ${a[m]} 当作最小值。`, `Pass ${i + 1}: take ${a[m]} as the smallest so far.`));
          for (let j = i + 1; j < a.length; j += 1) {
            comps += 1;
            const smaller = a[j] < a[m];
            if (smaller) m = j;
            snap({ sorted: i, min: a[m], hot: [a[j]], count: comps }, smaller
              ? tr(`比较 ${a[j]}：比之前的最小值小，记下 ${a[j]}（第 ${comps} 次比较）。`, `Compare ${a[j]}: smaller, so remember ${a[j]} (comparison ${comps}).`)
              : tr(`比较 ${a[j]}：不比 ${a[m]} 小（第 ${comps} 次比较）。`, `Compare ${a[j]}: not smaller than ${a[m]} (comparison ${comps}).`));
          }
          const moved = m !== i;
          [a[i], a[m]] = [a[m], a[i]];
          snap({ sorted: i + 1, count: comps, hot: [a[i]] }, moved
            ? tr(`把最小值 ${a[i]} 换到第 ${i} 位。`, `Swap the minimum ${a[i]} into position ${i}.`)
            : tr(`最小值 ${a[i]} 已经在第 ${i} 位，不用交换。`, `The minimum ${a[i]} is already in position ${i}; no swap needed.`));
        }
        snap({ sorted: 4, count: comps, done: true }, tr(`完成：<b>${list(a)}</b>。一共比较 ${comps} 次；就算输入本来就排好了，也还是 ${comps} 次。`, `Done: <b>${list(a)}</b>. ${comps} comparisons, and still ${comps} even if the input were already sorted.`));
      }
      return { frames, mount: (stage) => {
        const row = h('div', 'bars');
        const counter = h('div', 'viz-counter');
        stage.append(row, counter);
        const bars = Object.fromEntries([5, 2, 4, 1].map((v) => { const b = h('div', 'bar', `<span>${v}</span>`); b.style.height = `${28 + v * 22}px`; row.append(b); return [v, b]; }));
        return (f) => {
          f.order.forEach((v, i) => {
            const b = bars[v];
            b.style.transform = `translate(${i * 100}%, ${f.key === v ? '-26px' : '0'})`;
            b.classList.toggle('is-sorted', f.done || i < f.sorted);
            b.classList.toggle('is-key', f.key === v || f.min === v);
            b.classList.toggle('is-hot', (f.hot || []).includes(v));
          });
          counter.textContent = mode === 'insertion' ? tr(`移动 ${f.count} 次`, `${f.count} shifts`) : tr(`比较 ${f.count} 次`, `${f.count} comparisons`);
        };
      } };
    },
  };

  /* ------------------------------------------------------------ COMP2123 · merge sort */
  KINDS.merge = {
    build() {
      const row = (label, groups, extra = {}) => ({ label, groups, ...extra });
      const split = [row(tr('输入', 'input'), [[8, 3, 7, 1]]), row(tr('分', 'split'), [[8, 3], [7, 1]]), row(tr('分', 'split'), [[8], [3], [7], [1]])];
      const frames = [
        { rows: split.slice(0, 1), msg: tr('要排序 <b>[8, 3, 7, 1]</b>。', 'Sort <b>[8, 3, 7, 1]</b>.') },
        { rows: split.slice(0, 2), msg: tr('分成两半：[8, 3] 和 [7, 1]。', 'Split into halves: [8, 3] and [7, 1].') },
        { rows: split, msg: tr('再分，直到每组只剩一个数。单个数本来就是有序的。', 'Split again until each group holds one value. A single value is already sorted.') },
        { rows: [...split, row(tr('合', 'merge'), [[3, 8], []])], hot: [[2, 0], [2, 1]], msg: tr('合并 [8] 和 [3]：比较 8 和 3，先放 3，再放 8。', 'Merge [8] and [3]: compare 8 with 3, output 3, then 8.') },
        { rows: [...split, row(tr('合', 'merge'), [[3, 8], [1, 7]])], hot: [[2, 2], [2, 3]], msg: tr('合并 [7] 和 [1]，得到 [1, 7]。', 'Merge [7] and [1] into [1, 7].') },
        { rows: [...split, row(tr('合', 'merge'), [[3, 8], [1, 7]]), row(tr('合', 'merge'), [[1]])], hot: [[3, 0, 0], [3, 1, 0]], msg: tr('最后一次合并：比较两组的队首 3 和 1，输出较小的 1。', 'Final merge: compare the fronts 3 and 1, output the smaller, 1.') },
        { rows: [...split, row(tr('合', 'merge'), [[3, 8], [1, 7]]), row(tr('合', 'merge'), [[1, 3]])], hot: [[3, 0, 0], [3, 1, 1]], msg: tr('比较 3 和 7，输出 3。', 'Compare 3 with 7, output 3.') },
        { rows: [...split, row(tr('合', 'merge'), [[3, 8], [1, 7]]), row(tr('合', 'merge'), [[1, 3, 7]])], hot: [[3, 0, 1], [3, 1, 1]], msg: tr('比较 8 和 7，输出 7。', 'Compare 8 with 7, output 7.') },
        { rows: [...split, row(tr('合', 'merge'), [[3, 8], [1, 7]]), row(tr('结果', 'result'), [[1, 3, 7, 8]], { done: true })], msg: tr('左边只剩 8，直接接在后面：<b>[1, 3, 7, 8]</b>。每次只比较两组的队首，因为两组各自已经有序。', 'Only 8 is left, so append it: <b>[1, 3, 7, 8]</b>. Only the fronts are compared because each half is already sorted.') },
        { rows: [...split, row(tr('合', 'merge'), [[3, 8], [1, 7]]), row(tr('结果', 'result'), [[1, 3, 7, 8]], { done: true })], levels: true, msg: tr('4 个数要合并 2 层（log₂4 = 2），每层最多处理 4 个数：这就是 n log n 的来历。', 'Four values need two merge levels (log₂4 = 2), and each level handles at most four values: that is where n log n comes from.') },
      ];
      return { frames, mount: (stage) => (f) => {
        stage.innerHTML = '';
        f.rows.forEach((r, ri) => {
          const line = h('div', `merge-row${r.done ? ' is-done' : ''}${f.levels && ri >= 3 ? ' is-level' : ''}`);
          line.append(h('span', 'merge-label', r.label));
          r.groups.forEach((g, gi) => {
            const group = h('div', 'merge-group');
            g.forEach((v, vi) => {
              const hot = (f.hot || []).some(([hr, hg, hv]) => hr === ri && hg === gi && (hv === undefined || hv === vi));
              group.append(h('span', `chip${hot ? ' is-hot' : ''}`, String(v)));
            });
            if (!g.length) group.classList.add('is-empty');
            line.append(group);
          });
          stage.append(line);
        });
      } };
    },
  };

  /* ------------------------------------------------------------ COMP2123 · breadth-first search */
  KINDS.bfs = {
    build() {
      const P = { S: [50, 110], A: [175, 46], B: [175, 174], C: [305, 46], D: [305, 174], E: [430, 110] };
      const edges = [['S', 'A'], ['S', 'B'], ['A', 'C'], ['B', 'D'], ['C', 'E'], ['D', 'E']];
      const f = (cur, d, queue, done, tree, text, extra = {}) => ({ cur, d, queue, done, tree, msg: text, ...extra });
      const frames = [
        f(null, { S: 0 }, ['S'], [], [], tr('从 S 出发：d[S] = 0，队列是 [S]。其余顶点的距离先记作 ∞。', 'Start at S: d[S] = 0 and the queue is [S]. Every other vertex starts at ∞.')),
        f('S', { S: 0, A: 1, B: 1 }, ['A', 'B'], ['S'], ['S-A', 'S-B'], tr('取出 S，第一次发现 A 和 B，距离都是 1。', 'Remove S. A and B are discovered for the first time, both at distance 1.')),
        f('A', { S: 0, A: 1, B: 1, C: 2 }, ['B', 'C'], ['S', 'A'], ['S-A', 'S-B', 'A-C'], tr('取出 A，发现 C，距离 2。', 'Remove A and discover C at distance 2.')),
        f('B', { S: 0, A: 1, B: 1, C: 2, D: 2 }, ['C', 'D'], ['S', 'A', 'B'], ['S-A', 'S-B', 'A-C', 'B-D'], tr('取出 B，发现 D，距离 2。', 'Remove B and discover D at distance 2.')),
        f('C', { S: 0, A: 1, B: 1, C: 2, D: 2, E: 3 }, ['D', 'E'], ['S', 'A', 'B', 'C'], ['S-A', 'S-B', 'A-C', 'B-D', 'C-E'], tr('取出 C，发现 E，距离 3。', 'Remove C and discover E at distance 3.')),
        f('D', { S: 0, A: 1, B: 1, C: 2, D: 2, E: 3 }, ['E'], ['S', 'A', 'B', 'C', 'D'], ['S-A', 'S-B', 'A-C', 'B-D', 'C-E'], tr('取出 D，看到 E 已经标记过，不再重复入队。', 'Remove D. E is already marked, so it is not enqueued again.'), { look: 'D-E' }),
        f('E', { S: 0, A: 1, B: 1, C: 2, D: 2, E: 3 }, [], ['S', 'A', 'B', 'C', 'D', 'E'], ['S-A', 'S-B', 'A-C', 'B-D', 'C-E'], tr('取出 E，没有新邻居，队列空了。', 'Remove E. No new neighbours, and the queue is empty.')),
        f(null, { S: 0, A: 1, B: 1, C: 2, D: 2, E: 3 }, [], ['S', 'A', 'B', 'C', 'D', 'E'], ['S-A', 'S-B', 'A-C', 'B-D', 'C-E'], tr('沿 parent 往回走：E ← C ← A ← S，最短距离是 3。另一条 S–B–D–E 一样短。', 'Follow parents back: E ← C ← A ← S, a shortest distance of 3. The route S–B–D–E is equally short.'), { path: ['S-A', 'A-C', 'C-E'] }),
      ];
      return { frames, mount: (stage) => {
        const svg = s('svg', { viewBox: '0 0 480 220', class: 'graph' });
        const lines = Object.fromEntries(edges.map(([u, v]) => { const l = s('line', { x1: P[u][0], y1: P[u][1], x2: P[v][0], y2: P[v][1] }); svg.append(l); return [`${u}-${v}`, l]; }));
        const nodes = Object.fromEntries(Object.entries(P).map(([k, [x, y]]) => {
          const g = s('g', { class: 'node', transform: `translate(${x} ${y})` });
          g.append(s('circle', { r: 21 }), s('text', { class: 'name', y: 5 }, k), s('text', { class: 'dist', y: -29 }, '∞'));
          svg.append(g);
          return [k, g];
        }));
        const queue = h('div', 'queue');
        stage.append(svg, queue);
        return (fr) => {
          Object.entries(lines).forEach(([k, l]) => {
            l.setAttribute('class', (fr.path || []).includes(k) ? 'is-path' : fr.tree.includes(k) ? 'is-tree' : fr.look === k ? 'is-look' : '');
          });
          Object.entries(nodes).forEach(([k, g]) => {
            const state = fr.cur === k ? 'is-current' : fr.done.includes(k) ? 'is-done' : fr.queue.includes(k) ? 'is-queued' : '';
            g.setAttribute('class', `node ${state}`);
            g.querySelector('.dist').textContent = k in fr.d ? `d=${fr.d[k]}` : 'd=∞';
          });
          queue.innerHTML = `<span>${tr('队列', 'Queue')}</span>${fr.queue.length ? fr.queue.map((q) => `<b>${q}</b>`).join('') : `<em>${tr('空', 'empty')}</em>`}`;
        };
      } };
    },
  };

  /* ------------------------------------------------------------ COMP2123 · linear probing and deletion */
  KINDS.probe = {
    options: () => [{ value: 'tomb', label: tr('删除时留墓碑', 'Delete with a tombstone') }, { value: 'empty', label: tr('删除时直接清空', 'Delete by emptying') }],
    build(mode) {
      const t = Array(7).fill(null);
      const frames = [];
      const snap = (probe, text, extra = {}) => frames.push({ table: [...t], probe, msg: text, ...extra });
      snap([], tr('7 个槽位，h(k) = k mod 7。10、17、24 除以 7 都余 3。', 'Seven slots with h(k) = k mod 7. 10, 17 and 24 all leave remainder 3.'));
      [10, 17, 24].forEach((k) => {
        let i = k % 7;
        const seen = [];
        while (t[i] !== null) { seen.push(i); i = (i + 1) % 7; }
        seen.push(i);
        t[i] = k;
        snap(seen, seen.length > 1
          ? tr(`插入 ${k}：槽 ${seen.slice(0, -1).join('、')} 已被占用，往后探测，放进槽 ${i}。`, `Insert ${k}: slot${seen.length > 2 ? 's' : ''} ${seen.slice(0, -1).join(', ')} taken, so probe on and place it in slot ${i}.`)
          : tr(`插入 ${k}：${k} mod 7 = 3，槽 3 是空的，直接放入。`, `Insert ${k}: ${k} mod 7 = 3 and slot 3 is free.`), { hit: i });
      });
      snap([3, 4, 5], tr('查找 24：依次看槽 3（10）、槽 4（17）、槽 5，找到了，用了 3 次探测。', 'Find 24: inspect slot 3 (10), slot 4 (17), then slot 5. Found after three probes.'), { hit: 5 });
      t[4] = mode === 'tomb' ? 'tomb' : null;
      snap([4], mode === 'tomb'
        ? tr('删除 17：在槽 4 留下墓碑 †，表示“这里以前有过元素，查找请继续”。', 'Delete 17: leave a tombstone † in slot 4, meaning "something was here, keep searching".')
        : tr('删除 17：把槽 4 直接清空，看起来和从没用过一样。', 'Delete 17: empty slot 4, so it now looks never used.'));
      if (mode === 'tomb') {
        snap([3, 4, 5], tr('再查找 24：槽 3 是 10，槽 4 是墓碑，继续往后，槽 5 找到 24。<b>结果正确。</b>', 'Find 24 again: slot 3 holds 10, slot 4 is a tombstone so keep going, and slot 5 holds 24. <b>Correct.</b>'), { hit: 5 });
      } else {
        snap([3, 4], tr('再查找 24：槽 3 是 10，槽 4 是空的，于是停下，报告 24 不存在。<b>这是错的</b>，24 明明在槽 5。', 'Find 24 again: slot 3 holds 10, slot 4 is empty, so the search stops and reports 24 absent. <b>Wrong</b>: 24 is in slot 5.'), { miss: true });
      }
      return { frames, mount: (stage) => {
        const row = h('div', 'slots');
        const cells = [...Array(7)].map((_, i) => { const c = h('div', 'slot', `<small>${i}</small><b></b>`); row.append(c); return c; });
        const trail = h('div', 'probe-trail');
        stage.append(row, trail);
        return (f) => {
          cells.forEach((c, i) => {
            const v = f.table[i];
            c.querySelector('b').textContent = v === 'tomb' ? '†' : v ?? '';
            c.className = `slot${v === 'tomb' ? ' is-tomb' : v !== null ? ' is-full' : ''}${f.probe.includes(i) ? ' is-probe' : ''}${f.hit === i ? ' is-hit' : ''}${f.miss && i === f.probe[f.probe.length - 1] ? ' is-miss' : ''}`;
          });
          trail.innerHTML = f.probe.length ? `<span>${tr('探测顺序', 'Probe order')}</span>${f.probe.map((p) => `<b>${p}</b>`).join('<i>→</i>')}` : '';
        };
      } };
    },
  };

  /* ------------------------------------------------------------ COMP2017 · two-dimensional array layout */
  KINDS.layout = {
    build() {
      const f = (ptr, text, extra = {}) => ({ ptr, msg: text, ...extra });
      const frames = [
        f(null, tr('<code>int grid[2][3] = {{2,4,6},{8,10,12}};</code> 在内存里是连续的 6 个 int，共 2×3×4 = 24 字节。', '<code>int grid[2][3] = {{2,4,6},{8,10,12}};</code> is six adjacent ints: 2×3×4 = 24 bytes.'), { all: true }),
        f(null, tr('按行存放：先是第 0 行 {2, 4, 6}，紧接着第 1 行 {8, 10, 12}。', 'Row-major order: row 0 {2, 4, 6}, then row 1 {8, 10, 12} right after it.'), { rows: true }),
        f(null, tr('<code>grid[1][2]</code> 的字节偏移 = (1×3 + 2)×4 = 20。', 'The byte offset of <code>grid[1][2]</code> is (1×3 + 2)×4 = 20.'), { rows: true, hot: [5] }),
        f({ name: 'row', at: 0, span: 3 }, tr('<code>int (*row)[3] = grid;</code> row 指向“一整行”，类型记住了每行有 3 个 int。', '<code>int (*row)[3] = grid;</code> row points to a whole row; its type knows each row holds 3 ints.'), { rows: true }),
        f({ name: 'row + 1', at: 3, span: 3 }, tr('<code>row + 1</code> 前进 12 个字节（一整行），指向第 1 行。<code>row[1][2]</code> 读到 12。', '<code>row + 1</code> moves 12 bytes, one whole row, to row 1. <code>row[1][2]</code> reads 12.'), { rows: true, hot: [5] }),
        f({ name: 'p', at: 0, span: 1 }, tr('<code>int *p = grid[0];</code> p 指向第 0 行的第一个 int。', '<code>int *p = grid[0];</code> p points to the first int of row 0.'), { rows: true }),
        f({ name: 'p + 1', at: 1, span: 1 }, tr('<code>p + 1</code> 只前进 4 个字节，也就是一个 int。', '<code>p + 1</code> moves only 4 bytes: one int.'), { rows: true }),
        f({ name: 'p + 3', at: 3, span: 1, warn: true }, tr('<code>p + 3</code> 是第 0 行的“尾后”指针：可以拿来比较，但不能解引用去读下一行。要访问第 1 行，用带行类型的指针和下标。', '<code>p + 3</code> is row 0’s one-past pointer: fine to compare, not to dereference into the next row. Use the row-aware type and indices for row 1.'), { rows: true }),
      ];
      return { frames, mount: (stage) => {
        const wrap = h('div', 'mem');
        const ptr = h('div', 'mem-ptr');
        const cells = h('div', 'mem-cells');
        const vals = [2, 4, 6, 8, 10, 12];
        const items = vals.map((v, i) => { const c = h('div', 'mem-cell', `<b>${v}</b><small>+${i * 4}</small>`); cells.append(c); return c; });
        const rows = h('div', 'mem-rows', `<span>${tr('第 0 行', 'row 0')} · 0–11</span><span>${tr('第 1 行', 'row 1')} · 12–23</span>`);
        wrap.append(ptr, cells, rows);
        stage.append(wrap);
        return (f) => {
          items.forEach((c, i) => c.className = `mem-cell${f.all ? ' is-all' : ''}${(f.hot || []).includes(i) ? ' is-hot' : ''}${f.ptr && i >= f.ptr.at && i < f.ptr.at + f.ptr.span ? (f.ptr.warn ? ' is-warn' : ' is-pointed') : ''}`);
          rows.classList.toggle('is-on', !!f.rows);
          ptr.className = `mem-ptr${f.ptr ? ' is-on' : ''}${f.ptr && f.ptr.warn ? ' is-warn' : ''}`;
          if (f.ptr) {
            ptr.style.left = `${(f.ptr.at / 6) * 100}%`;
            ptr.style.width = `${(f.ptr.span / 6) * 100}%`;
            ptr.innerHTML = `<span>${f.ptr.name}${f.ptr.warn ? ' ⚠' : ''}</span>`;
          }
        };
      } };
    },
  };

  /* ------------------------------------------------------------ INFO1113 · copied references */
  KINDS.refs = {
    build() {
      const code = ['int[] scores = {6, 8};', 'change(scores);', 'static void change(int[] x) {', '    x[0] = 10;', '    x = new int[]{1, 2};', '}', tr('// 回到调用处', '// back in the caller')];
      const f = (line, frames, heap, text, extra = {}) => ({ line, stack: frames, heap, msg: text, ...extra });
      const A = (v) => ({ id: 'A', cells: v });
      const frames = [
        f(0, [{ name: 'main', vars: [['scores', 'A']] }], [A([6, 8])], tr('scores 里存的不是数组本身，而是指向数组 A 的引用。', 'scores does not hold the array itself, only a reference to array A.')),
        f(1, [{ name: 'main', vars: [['scores', 'A']] }, { name: 'change', vars: [['x', 'A']] }], [A([6, 8])], tr('调用 change：把 scores 里的引用<b>复制</b>给参数 x。两个变量指向同一个数组。', 'Calling change <b>copies</b> the reference in scores into parameter x. Both variables point at the same array.')),
        f(3, [{ name: 'main', vars: [['scores', 'A']] }, { name: 'change', vars: [['x', 'A']] }], [A([10, 8])], tr('<code>x[0] = 10</code> 修改的是共享的数组 A，所以 scores 也看得到 [10, 8]。', '<code>x[0] = 10</code> changes the shared array A, so scores sees [10, 8] too.'), { hot: 'A0' }),
        f(4, [{ name: 'main', vars: [['scores', 'A']] }, { name: 'change', vars: [['x', 'B']] }], [A([10, 8]), { id: 'B', cells: [1, 2] }], tr('<code>x = new int[]{1, 2}</code> 只改了局部变量 x，让它指向新数组 B；scores 不受影响。', '<code>x = new int[]{1, 2}</code> only redirects the local x to a new array B; scores is untouched.'), { moved: 'x' }),
        f(5, [{ name: 'main', vars: [['scores', 'A']] }], [A([10, 8]), { id: 'B', cells: [1, 2], gone: true }], tr('方法返回，x 随调用记录一起消失；B 已经没有任何引用。', 'The method returns and x disappears with its frame; nothing refers to B any more.')),
        f(6, [{ name: 'main', vars: [['scores', 'A']] }], [A([10, 8])], tr('scores 仍然指向 A，内容是 <b>[10, 8]</b>。修改共享对象和给参数重新赋值是两回事，这就是 Java 的“按值传递引用”。', 'scores still refers to A, which holds <b>[10, 8]</b>. Mutating a shared object and reassigning a parameter are different: Java passes references by value.')),
      ];
      return { frames, mount: (stage) => {
        const codeBox = h('ol', 'refs-code', code.map((c) => `<li><code>${c.replace(/</g, '&lt;')}</code></li>`).join(''));
        const mem = h('div', 'refs-mem');
        const stack = h('div', 'refs-col', `<span class="refs-title">${tr('栈：调用记录', 'Stack: call frames')}</span>`);
        const heap = h('div', 'refs-col', `<span class="refs-title">${tr('堆：对象', 'Heap: objects')}</span>`);
        const svg = s('svg', { class: 'refs-arrows' });
        const defs = s('defs');
        const marker = s('marker', { id: `arrow-${Math.random().toString(36).slice(2)}`, viewBox: '0 0 10 10', refX: 9, refY: 5, markerWidth: 7, markerHeight: 7, orient: 'auto-start-reverse' });
        marker.append(s('path', { d: 'M0 0L10 5L0 10z' }));
        defs.append(marker);
        svg.append(defs);
        mem.append(stack, heap, svg);
        stage.append(codeBox, mem);
        let last = null;
        const arrows = () => {
          if (!last) return;
          [...svg.querySelectorAll('path.arrow')].forEach((p) => p.remove());
          const box = mem.getBoundingClientRect();
          svg.setAttribute('viewBox', `0 0 ${box.width} ${box.height}`);
          mem.querySelectorAll('[data-ref]').forEach((v) => {
            const target = mem.querySelector(`[data-obj="${v.dataset.ref}"]`);
            if (!target) return;
            const a = v.getBoundingClientRect(); const b = target.getBoundingClientRect();
            const x1 = a.right - box.left - 6; const y1 = a.top + a.height / 2 - box.top;
            const x2 = b.left - box.left - 2; const y2 = b.top + b.height / 2 - box.top;
            const mid = (x1 + x2) / 2;
            svg.append(s('path', { class: `arrow${v.dataset.moved ? ' is-moved' : ''}`, d: `M${x1} ${y1}C${mid} ${y1} ${mid} ${y2} ${x2} ${y2}`, 'marker-end': `url(#${marker.id})` }));
          });
        };
        window.addEventListener('resize', arrows);
        return (f) => {
          last = f;
          [...codeBox.children].forEach((li, i) => li.classList.toggle('is-line', i === f.line));
          stack.querySelectorAll('.frame').forEach((n) => n.remove());
          f.stack.forEach((fr) => stack.append(h('div', 'frame', `<span>${fr.name}</span>${fr.vars.map(([n, ref]) => `<div class="var" data-ref="${ref}"${f.moved === n ? ' data-moved="1"' : ''}><code>${n}</code><i>●</i></div>`).join('')}`)));
          heap.querySelectorAll('.obj').forEach((n) => n.remove());
          f.heap.forEach((o) => heap.append(h('div', `obj${o.gone ? ' is-gone' : ''}`, `<span>${tr('数组', 'array')} ${o.id}</span><div class="cells">${o.cells.map((c, i) => `<b class="${f.hot === o.id + i ? 'is-hot' : ''}">${c}</b>`).join('')}</div>`)));
          heap.querySelectorAll('.obj').forEach((n, i) => { n.dataset.obj = f.heap[i].id; });
          requestAnimationFrame(arrows);
        };
      } };
    },
  };

  /* ------------------------------------------------------------ COMP2022 · a DFA for an odd number of 1s */
  KINDS.dfa = {
    options: () => ['10110', '0110', '111', ''].map((w) => ({ value: w, label: w || 'ε' })),
    custom(apply) {
      const label = h('label', 'viz-input', `<span>${tr('自己输入', 'Your input')}</span>`);
      const input = h('input');
      input.type = 'text';
      input.inputMode = 'numeric';
      input.maxLength = 12;
      input.placeholder = '0/1';
      input.setAttribute('aria-label', tr('输入一串 0 和 1', 'Type a string of 0s and 1s'));
      input.addEventListener('input', () => { input.value = input.value.replace(/[^01]/g, ''); apply(input.value); });
      label.append(input);
      label.reset = () => { input.value = ''; };
      return label;
    },
    build(w) {
      const frames = [{ state: 'E', head: -1, trail: ['E'], msg: tr(`输入 <b>${w || 'ε（空串）'}</b>。从起始状态 E 出发：E 表示“读过的 1 是偶数个”。`, `Input <b>${w || 'ε (empty)'}</b>. Start in E, which means "an even number of 1s so far".`) }];
      let q = 'E';
      [...w].forEach((c, i) => {
        const from = q;
        if (c === '1') q = q === 'E' ? 'O' : 'E';
        frames.push({ state: q, head: i, edge: `${from}${c}`, trail: [...frames[frames.length - 1].trail, q], msg: c === '1'
          ? tr(`读到 1：${from} → ${q}，1 的个数从${from === 'E' ? '偶数变成奇数' : '奇数变成偶数'}。`, `Read 1: ${from} → ${q}; the count of 1s turns ${from === 'E' ? 'odd' : 'even'}.`)
          : tr(`读到 0：留在 ${q}，1 的个数不变。`, `Read 0: stay in ${q}; the count of 1s is unchanged.`) });
      });
      const ok = q === 'O';
      frames.push({ state: q, head: w.length, trail: frames[frames.length - 1].trail, end: ok ? 'accept' : 'reject', msg: ok
        ? tr(`读完了，停在 O（接受状态）：输入里有奇数个 1，<b>接受</b>。状态序列 ${frames[frames.length - 1].trail.join(' → ')}。`, `Finished in O, the accepting state: an odd number of 1s, so <b>accept</b>. States: ${frames[frames.length - 1].trail.join(' → ')}.`)
        : tr(`读完了，停在 E：1 是偶数个，<b>不接受</b>。状态序列 ${frames[frames.length - 1].trail.join(' → ')}。`, `Finished in E: an even number of 1s, so <b>reject</b>. States: ${frames[frames.length - 1].trail.join(' → ')}.`) });
      return { frames, mount: (stage) => {
        const svg = s('svg', { viewBox: '0 0 460 190', class: 'dfa' });
        const defs = s('defs');
        const id = `dfa-${Math.random().toString(36).slice(2)}`;
        const marker = s('marker', { id, viewBox: '0 0 10 10', refX: 9, refY: 5, markerWidth: 7, markerHeight: 7, orient: 'auto' });
        marker.append(s('path', { d: 'M0 0L10 5L0 10z' }));
        defs.append(marker);
        svg.append(defs);
        const edge = (key, d, lx, ly, label) => { const g = s('g', { class: 'edge', 'data-edge': key }); g.append(s('path', { d, 'marker-end': `url(#${id})` }), s('text', { x: lx, y: ly }, label)); svg.append(g); return g; };
        edge('start', 'M40 110H102', 0, 0, '');
        edge('E1', 'M160 88C200 40 260 40 300 88', 230, 46, '1');
        edge('O1', 'M300 132C260 180 200 180 160 132', 230, 182, '1');
        edge('E0', 'M118 86C100 30 160 30 142 86', 130, 34, '0');
        edge('O0', 'M318 86C300 30 360 30 342 86', 330, 34, '0');
        const node = (k, x, accept) => { const g = s('g', { class: 'state', transform: `translate(${x} 110)` }); g.append(s('circle', { r: 26 })); if (accept) g.append(s('circle', { r: 20, class: 'inner' })); g.append(s('text', { y: 6 }, k)); svg.append(g); return g; };
        const states = { E: node('E', 130, false), O: node('O', 330, true) };
        const tape = h('div', 'tape');
        stage.append(svg, tape);
        return (f) => {
          Object.entries(states).forEach(([k, g]) => g.setAttribute('class', `state${f.state === k ? ' is-on' : ''}${f.end && f.state === k ? ` is-${f.end}` : ''}`));
          svg.querySelectorAll('.edge').forEach((g) => g.classList.toggle('is-on', g.dataset.edge === f.edge));
          tape.innerHTML = (w ? [...w].map((c, i) => `<b class="${i === f.head ? 'is-head' : i < f.head ? 'is-read' : ''}">${c}</b>`).join('') : '<em>ε</em>') + (f.end ? `<span class="verdict is-${f.end}">${f.end === 'accept' ? tr('接受', 'accept') : tr('不接受', 'reject')}</span>` : '');
        };
      } };
    },
  };

  /* ------------------------------------------------------------ START · one learning step on L(w) = (w − 3)² */
  KINDS.descent = {
    options: () => [0.1, 0.5, 0.9, 1.1].map((v) => ({ value: v, label: `η = ${v}` })),
    build(eta) {
      const L = (w) => (w - 3) ** 2;
      const frames = [];
      let w = 0;
      const trail = [];
      const steps = eta > 1 ? 4 : 9; // past this a diverging run leaves the plot
      for (let k = 0; k < steps; k += 1) {
        const g = 2 * (w - 3);
        const next = w - eta * g;
        trail.push(w);
        frames.push({ w, trail: [...trail], g, msg: k === 0
          ? tr(`从 w = 0 开始：损失 (0 − 3)² = 9，斜率 2(0 − 3) = −6。走一步：w ← 0 − ${eta} × (−6) = <b>${fmt(next)}</b>。`, `Start at w = 0: loss (0 − 3)² = 9, slope 2(0 − 3) = −6. One step: w ← 0 − ${eta} × (−6) = <b>${fmt(next)}</b>.`)
          : tr(`w = ${fmt(w)}，损失 ${fmt(L(w))}，斜率 ${fmt(g)}。下一步 w = <b>${fmt(next)}</b>。`, `w = ${fmt(w)}, loss ${fmt(L(w))}, slope ${fmt(g)}. Next w = <b>${fmt(next)}</b>.`) });
        if (Math.abs(g) < 1e-9) break;
        w = next;
      }
      const end = frames[frames.length - 1];
      const verdict = eta === 0.5
        ? tr('η = 0.5 时一步正好落到谷底 w = 3：这个损失的曲率刚好配这个步长。', 'With η = 0.5 one step lands exactly on the minimum w = 3: the step matches this curve’s curvature.')
        : eta === 1.1
          ? tr('η = 1.1 时步子太大：每一步都越过谷底，而且越跳越远，损失越来越大。', 'With η = 1.1 the steps are too big: each one overshoots the minimum by more, and the loss grows.')
          : eta === 0.9
            ? tr('η = 0.9 时会在谷底两边来回跳，但幅度越来越小，最后还是收敛到 3。', 'With η = 0.9 it bounces across the minimum, but each bounce is smaller, so it still converges to 3.')
            : tr('η = 0.1 时每一步都朝谷底走一点，越靠近，斜率越小，步子也越小。', 'With η = 0.1 every step moves a little closer; the slope shrinks near the minimum, so the steps do too.');
      frames.push({ ...end, msg: verdict, last: true });
      return { frames, mount: (stage) => {
        const W = 460; const H = 220; const x = (w) => 30 + ((w + 2.5) / 11) * (W - 50); const y = (l) => H - 26 - Math.min(l, 30) / 30 * (H - 50);
        const svg = s('svg', { viewBox: `0 0 ${W} ${H}`, class: 'curve' });
        let d = '';
        for (let v = -2.5; v <= 8.501; v += 0.1) d += `${d ? 'L' : 'M'}${x(v).toFixed(1)} ${y(L(v)).toFixed(1)}`;
        svg.append(s('line', { class: 'axis', x1: 30, y1: H - 26, x2: W - 20, y2: H - 26 }), s('path', { class: 'loss', d }), s('line', { class: 'min', x1: x(3), y1: H - 26, x2: x(3), y2: 18 }), s('text', { class: 'tick', x: x(3), y: H - 8 }, 'w = 3'), s('text', { class: 'tick', x: x(0), y: H - 8 }, '0'));
        const path = s('path', { class: 'jumps' });
        const tangent = s('line', { class: 'tangent' });
        const ball = s('circle', { class: 'ball', r: 7 });
        const label = s('text', { class: 'ball-label' });
        svg.append(path, tangent, ball, label);
        stage.append(svg);
        return (f) => {
          const pts = f.trail.map((v) => [x(Math.max(-2.5, Math.min(8.5, v))), y(L(v))]);
          path.setAttribute('d', pts.map((p, i) => `${i ? 'L' : 'M'}${p[0].toFixed(1)} ${p[1].toFixed(1)}`).join(''));
          const cw = Math.max(-2.5, Math.min(8.5, f.w));
          const [bx, by] = [x(cw), y(L(f.w))];
          ball.setAttribute('cx', bx); ball.setAttribute('cy', by);
          const dx = 0.9; const slope = 2 * (cw - 3);
          tangent.setAttribute('x1', x(cw - dx)); tangent.setAttribute('y1', y(L(cw) - slope * dx));
          tangent.setAttribute('x2', x(cw + dx)); tangent.setAttribute('y2', y(L(cw) + slope * dx));
          label.setAttribute('x', bx); label.setAttribute('y', by - 14);
          label.textContent = `w = ${fmt(f.w)}`;
        };
      } };
    },
  };

  /* ------------------------------------------------------------ ML · gradient descent fits a line to two points */
  KINDS.linefit = {
    options: () => [0.1, 0.3].map((v) => ({ value: v, label: `η = ${v}` })),
    build(eta) {
      const z = [-1, 1]; const yv = [1, 3];
      let w = 0; let b = 0;
      const frames = []; const losses = [];
      for (let k = 0; k <= 12; k += 1) {
        const p = z.map((zi) => w * zi + b);
        const r = p.map((pi, i) => pi - yv[i]);
        const loss = (r[0] ** 2 + r[1] ** 2) / 2;
        const gw = (2 / 2) * (r[0] * z[0] + r[1] * z[1]);
        const gb = (2 / 2) * (r[0] + r[1]);
        losses.push(loss);
        const nw = w - eta * gw; const nb = b - eta * gb;
        frames.push({ w, b, losses: [...losses], msg: k === 0
          ? tr(`标准化后的输入是 −1 和 1，目标是 1 和 3。w = b = 0 时两个预测都是 0，损失 (1 + 9) / 2 = 5；g_w = ${fmt(gw)}，g_b = ${fmt(gb)}，更新后 w = <b>${fmt(nw)}</b>，b = <b>${fmt(nb)}</b>。`, `Standardised inputs are −1 and 1, targets 1 and 3. With w = b = 0 both predictions are 0 and the loss is (1 + 9) / 2 = 5; g_w = ${fmt(gw)}, g_b = ${fmt(gb)}, so w becomes <b>${fmt(nw)}</b> and b <b>${fmt(nb)}</b>.`)
          : tr(`第 ${k} 步：预测 ${fmt(p[0])} 和 ${fmt(p[1])}，损失 <b>${fmt(loss, 3)}</b>。`, `Step ${k}: predictions ${fmt(p[0])} and ${fmt(p[1])}, loss <b>${fmt(loss, 3)}</b>.`) });
        w = nw; b = nb;
      }
      frames.push({ ...frames[frames.length - 1], msg: tr('直线越来越接近同时穿过两个点的 y = z + 2（w = 1，b = 2）。损失下降只说明训练集拟合得更好，不等于模型在新数据上也好。', 'The line approaches y = z + 2 (w = 1, b = 2), which passes through both points. A falling training loss shows a better fit, not better results on new data.') });
      return { frames, mount: (stage) => {
        const W = 300; const H = 210; const X = (v) => 30 + ((v + 2) / 4) * (W - 50); const Y = (v) => H - 24 - ((v + 1) / 5) * (H - 44);
        const svg = s('svg', { viewBox: `0 0 ${W} ${H}`, class: 'fit' });
        svg.append(s('line', { class: 'axis', x1: 20, y1: Y(0), x2: W - 10, y2: Y(0) }), s('line', { class: 'axis', x1: X(0), y1: 10, x2: X(0), y2: H - 14 }), s('text', { class: 'tick', x: W - 16, y: Y(0) - 6 }, 'z'), s('text', { class: 'tick', x: X(0) + 10, y: 18 }, 'y'));
        const res = [0, 1].map(() => { const l = s('line', { class: 'residual' }); svg.append(l); return l; });
        const line = s('line', { class: 'fit-line' });
        svg.append(line);
        z.forEach((zi, i) => svg.append(s('circle', { class: 'pt', cx: X(zi), cy: Y(yv[i]), r: 6 })));
        const spark = s('svg', { viewBox: '0 0 150 210', class: 'spark' });
        const sp = s('path', { class: 'spark-line' });
        spark.append(s('text', { class: 'tick', x: 6, y: 16 }, tr('损失', 'Loss')), s('line', { class: 'axis', x1: 6, y1: 190, x2: 146, y2: 190 }), sp);
        const val = s('text', { class: 'spark-val', x: 146, y: 16 });
        spark.append(val);
        const row = h('div', 'fit-row');
        row.append(svg, spark);
        stage.append(row);
        return (f) => {
          line.setAttribute('x1', X(-2)); line.setAttribute('y1', Y(f.w * -2 + f.b)); line.setAttribute('x2', X(2)); line.setAttribute('y2', Y(f.w * 2 + f.b));
          z.forEach((zi, i) => { res[i].setAttribute('x1', X(zi)); res[i].setAttribute('x2', X(zi)); res[i].setAttribute('y1', Y(yv[i])); res[i].setAttribute('y2', Y(f.w * zi + f.b)); });
          sp.setAttribute('d', f.losses.map((l, i) => `${i ? 'L' : 'M'}${(10 + i * 11).toFixed(1)} ${(190 - (l / 5) * 160).toFixed(1)}`).join(''));
          val.textContent = fmt(f.losses[f.losses.length - 1], 3);
        };
      } };
    },
  };

  document.querySelectorAll('figure.viz').forEach(mount);
})();
