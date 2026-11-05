(() => {
  const root = document.documentElement;
  const chinese = root.lang.startsWith('zh');
  if (document.body.classList.contains('field-guide')) {
    try { localStorage.setItem('guoliang-language', chinese ? 'zh' : 'en'); } catch (_) {}
  }
  const button = document.querySelector('[data-theme-toggle]');
  const setTheme = (theme) => {
    root.dataset.theme = theme;
    if (button) {
      button.textContent = theme === 'dark' ? '☼' : '☾';
      button.setAttribute('aria-label', chinese ? (theme === 'dark' ? '切换到浅色主题' : '切换到深色主题') : `Switch to ${theme === 'dark' ? 'light' : 'dark'} theme`);
    }
  };
  let stored;
  try { stored = localStorage.getItem('guoliang-theme'); } catch (_) {}
  setTheme(stored === 'light' ? 'light' : 'dark');
  const setReadingSize = size => {
    root.dataset.readingSize = size;
    document.querySelectorAll('[data-reading-size]').forEach(control => {
      if (control.tagName === 'BUTTON') control.setAttribute('aria-pressed', String(control.dataset.readingSize === size));
    });
  };
  let readingSize;
  try { readingSize = localStorage.getItem('guoliang-reading-size'); } catch (_) {}
  setReadingSize(readingSize === 'large' ? 'large' : 'normal');
  document.querySelectorAll('button[data-reading-size]').forEach(control => control.addEventListener('click', () => {
    setReadingSize(control.dataset.readingSize);
    try { localStorage.setItem('guoliang-reading-size', control.dataset.readingSize); } catch (_) {}
  }));
  document.querySelectorAll('[data-copy-code]').forEach(control => control.addEventListener('click', async () => {
    const code = document.getElementById(control.dataset.copyCode);
    if (!code) return;
    try {
      await navigator.clipboard.writeText(code.textContent);
      control.textContent = chinese ? '已复制' : 'Copied';
    } catch (_) {
      control.textContent = chinese ? '请选择代码复制，或下载文件' : 'Select code to copy, or download';
    }
  }));
  button?.addEventListener('click', () => {
    const theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
    setTheme(theme);
    try { localStorage.setItem('guoliang-theme', theme); } catch (_) {}
  });
  // the "scroll sideways" hint only shows where a program is wider than its box
  const fit = () => document.querySelectorAll('.code-example').forEach(example => {
    const pre = example.querySelector('pre.code');
    if (pre) example.classList.toggle('fits', pre.scrollWidth <= pre.clientWidth + 1);
  });
  fit();
  let refit;
  window.addEventListener('resize', () => { clearTimeout(refit); refit = setTimeout(fit, 200); });
  document.addEventListener('click', event => { if (event.target.closest('[data-reading-size]')) requestAnimationFrame(fit); });
  const toc = document.querySelector('.toc details');
  if (toc && window.matchMedia('(max-width: 1000px)').matches) toc.open = false;
  document.querySelector('[data-print]')?.addEventListener('click', () => window.print());
  document.querySelectorAll('.language-switch a[data-language]').forEach(link => {
    link.addEventListener('click', () => {
      try { localStorage.setItem('guoliang-language', link.dataset.language); } catch (_) {}
      const sections = [...document.querySelectorAll('[data-reading-id]')];
      const anchored = sections.find(section => `#${section.id}` === window.location.hash);
      const anchorTop = anchored?.getBoundingClientRect().top;
      const current = anchored && anchorTop >= 0 && anchorTop < window.innerHeight * .8
        ? anchored
        : sections.map(section => {
          const box = section.getBoundingClientRect();
          return { section, visible: Math.max(0, Math.min(box.bottom, window.innerHeight) - Math.max(box.top, 100)) };
        }).sort((a, b) => b.visible - a.visible ||
          (a.section.contains(b.section) ? 1 : b.section.contains(a.section) ? -1 : 0)
        ).find(item => item.visible > 0)?.section;
      const target = new URL(link.href);
      target.hash = current?.id || window.location.hash;
      link.href = target.href;
    });
  });
  // Remember the chapter in view for the learning hub, and mark it in the contents rail.
  // A chapter counts as read once its end (the previous/next links) is on screen while you are in that chapter.
  const courseId = document.body.dataset.courseId;
  const chapters = [...document.querySelectorAll('article.topic[data-reading-id]')];
  if (courseId && chapters.length) {
    const tocLinks = new Map([...document.querySelectorAll('.toc ol a')].map(link => [link.getAttribute('href').slice(1), link]));
    let pending;
    let read = [];
    try { read = JSON.parse(localStorage.getItem('leon-learn-progress') || '{}').courses?.[courseId]?.read || []; } catch (_) {}
    const readLabel = chinese ? '（已读完）' : ' (read)';
    const markRead = () => tocLinks.forEach((link, id) => {
      const done = read.includes(id);
      link.classList.toggle('is-read', done);
      let note = link.querySelector('.sr-note');
      if (done && !note) { note = document.createElement('span'); note.className = 'sr-note'; note.textContent = readLabel; link.append(note); }
      if (!done && note) note.remove();
    });
    markRead();
    const track = () => {
      let current = null;
      for (const chapter of chapters) {
        if (chapter.offsetParent === null) continue; // hidden in phone chapter mode
        if (chapter.getBoundingClientRect().top <= 140) current = chapter; else break;
      }
      tocLinks.forEach((link, id) => link.classList.toggle('is-current', id === current?.id));
      // only the chapter being read can be finished: after a jump, the previous chapter's end may still peek in at the top
      const end = current?.querySelector('.topic-nav')?.getBoundingClientRect();
      if (end && end.top < window.innerHeight && end.bottom > 0 && !read.includes(current.id)) { read = [...read, current.id]; markRead(); }
      if (!current) return;
      try {
        const saved = JSON.parse(localStorage.getItem('leon-learn-progress') || '{}');
        saved.courses = saved.courses || {};
        // another tab of the same course may have marked chapters meanwhile: keep both
        read = [...new Set([...(saved.courses[courseId]?.read || []), ...read])];
        markRead();
        saved.courses[courseId] = {
          read,
          topic: current.id,
          title: current.querySelector('h2')?.textContent || '',
          url: `${location.pathname.split('/').slice(-2).join('/')}#${current.id}`,
          lang: chinese ? 'zh' : 'en',
          time: Date.now(),
        };
        saved.latest = courseId;
        localStorage.setItem('leon-learn-progress', JSON.stringify(saved));
      } catch (_) {}
    };
    window.addEventListener('scroll', () => { clearTimeout(pending); pending = setTimeout(track, 250); }, { passive: true });
    track();
  }
  if (document.body.classList.contains('reader')) {
    // a thin progress bar under the top bar
    const bar = document.createElement('div');
    bar.className = 'read-progress';
    bar.setAttribute('aria-hidden', 'true');
    document.body.append(bar);
    const paint = () => {
      const max = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.transform = `scaleX(${max > 0 ? Math.min(1, window.scrollY / max) : 0})`;
    };
    window.addEventListener('scroll', paint, { passive: true });
    window.addEventListener('resize', paint);
    paint();
    // where each chapter sits in the course: one dot per chapter, each a link
    chapters.forEach((chapter, index) => {
      const dots = document.createElement('nav');
      dots.className = 'chapter-dots';
      dots.setAttribute('aria-label', chinese ? '章节位置' : 'Chapter position');
      chapters.forEach((other, j) => {
        const dot = document.createElement('a');
        dot.href = `#${other.id}`;
        dot.title = other.querySelector('h2')?.textContent || '';
        if (j < index) dot.className = 'done';
        if (j === index) { dot.className = 'now'; dot.setAttribute('aria-current', 'step'); }
        dots.append(dot);
      });
      chapter.querySelector('.topic-head')?.append(dots);
    });
    // blocks rise into view as you read
    if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches && 'IntersectionObserver' in window) {
      const blocks = document.querySelectorAll('.topic > :not(.topic-head):not(h2), .framework .map-stage, .overview, .extension-card, .cheat-item');
      const seen = new IntersectionObserver(entries => entries.forEach(entry => {
        if (entry.isIntersecting) { entry.target.classList.add('in'); seen.unobserve(entry.target); }
      }), { rootMargin: '0px 0px -8% 0px' });
      blocks.forEach(block => {
        if (block.getBoundingClientRect().top > window.innerHeight) { block.classList.add('rise'); seen.observe(block); }
      });
    }
  }
  /* ---------- try first: answers stay folded unless the reader asks for them all ---------- */
  const folds = [...document.querySelectorAll('details.try-first')];
  if (folds.length) {
    const key = 'leon-learn-show-answers';
    const label = (on) => (chinese ? (on ? '重新折叠答案' : '展开全部答案') : (on ? 'Fold answers again' : 'Show all answers'));
    let open = false;
    try { open = localStorage.getItem(key) === '1'; } catch (_) {}
    const apply = () => { folds.forEach((d) => { d.open = open; }); document.querySelectorAll('[data-answers-toggle]').forEach((b) => { b.textContent = label(open); b.setAttribute('aria-pressed', String(open)); }); };
    const tools = document.querySelector('.reading-tools');
    const toggle = Object.assign(document.createElement('button'), { type: 'button', className: 'answers-toggle' });
    toggle.setAttribute('data-answers-toggle', '');
    toggle.addEventListener('click', () => { open = !open; try { localStorage.setItem(key, open ? '1' : '0'); } catch (_) {} apply(); });
    (tools || document.querySelector('.course-hero .actions'))?.append(toggle);
    apply();
    window.addEventListener('beforeprint', () => folds.forEach((d) => { d.dataset.wasOpen = d.open ? '1' : ''; d.open = true; }));
    window.addEventListener('afterprint', () => folds.forEach((d) => { d.open = d.dataset.wasOpen === '1'; }));
    // a link into a folded block must not land on hidden text
    const openFor = () => { const t = location.hash.length > 1 && document.getElementById(decodeURIComponent(location.hash.slice(1))); t?.closest?.('details.try-first')?.setAttribute('open', ''); };
    openFor();
    window.addEventListener('hashchange', openFor);
  }

  /* ---------- end of a chapter: practise it, and send its questions to the review queue ---------- */
  if (courseId && chapters.length) {
    const words = chinese ? { practise: '练这一章', add: '把这一章加入复习', added: '已加入复习', fail: '暂时加不上，稍后再试' } : { practise: 'Practise this chapter', add: 'Add this chapter to review', added: 'In your review queue', fail: 'Could not add it now; try later' };
    chapters.forEach((chapter) => {
      const nav = chapter.querySelector('.topic-nav');
      if (!nav) return;
      const bar = document.createElement('div');
      bar.className = 'chapter-study';
      const practise = Object.assign(document.createElement('a'), { href: `../learn/#/practice/${courseId}?topic=${chapter.id}`, textContent: `${words.practise} ↗` });
      const add = Object.assign(document.createElement('button'), { type: 'button', textContent: words.add });
      add.addEventListener('click', async () => {
        try {
          const data = await fetch(`../learn/data/${courseId}.json`).then((r) => r.json());
          const saved = JSON.parse(localStorage.getItem('leon-learn-srs') || '{}');
          data.cards.filter((c) => c.topic === chapter.id).forEach((c) => { const k = `${courseId}/${c.id}`; if (!(k in saved)) saved[k] = { fresh: true, added: Date.now() }; });
          localStorage.setItem('leon-learn-srs', JSON.stringify(saved));
          add.textContent = words.added;
          add.disabled = true;
        } catch (_) { add.textContent = words.fail; }
      });
      bar.append(practise, add);
      nav.before(bar);
    });
  }

  /* ---------- tap a word to see what it means: the first use per chapter of every glossary word in this course ---------- */
  if (courseId && chapters.length) {
    fetch(`../learn/data/terms-${courseId}.json`).then((r) => (r.ok ? r.json() : null)).then((all) => {
      const terms = all && all[chinese ? 'zh' : 'en'];
      if (!terms) return;
      const names = Object.keys(terms).filter((x) => x.length >= (chinese ? 2 : 3)).sort((a, b) => b.length - a.length);
      if (!names.length) return;
      const quoted = names.map((x) => x.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'));
      const pattern = new RegExp(chinese ? `(${quoted.join('|')})` : `(?<![\\w-])(${quoted.join('|')})(?![\\w-])`, chinese ? 'g' : 'gi');
      const lookup = new Map(names.map((x) => [x.toLowerCase(), terms[x]]));
      const pop = document.createElement('div');
      pop.className = 'term-pop';
      pop.hidden = true;
      pop.setAttribute('role', 'status');
      document.body.append(pop);
      let current = null;
      const close = () => { pop.hidden = true; current?.setAttribute('aria-expanded', 'false'); current = null; };
      const open = (button) => {
        const word = button.textContent;
        pop.textContent = '';
        const b = document.createElement('b');
        b.textContent = word;
        pop.append(b, ` ${lookup.get(word.toLowerCase()) || ''}`);
        pop.hidden = false;
        const box = button.getBoundingClientRect();
        pop.style.left = `${Math.max(8, Math.min(window.scrollX + box.left, window.scrollX + document.documentElement.clientWidth - pop.offsetWidth - 8))}px`;
        pop.style.top = `${window.scrollY + box.bottom + 6}px`;
        button.setAttribute('aria-expanded', 'true');
        current = button;
      };
      document.addEventListener('click', (event) => {
        const button = event.target.closest('.term');
        if (button) { if (current === button) close(); else { close(); open(button); } return; }
        if (!event.target.closest('.term-pop')) close();
      });
      document.addEventListener('keydown', (event) => { if (event.key === 'Escape') close(); });
      chapters.forEach((chapter) => {
        const used = new Set();
        const blocks = chapter.querySelectorAll('.story p, .principle p, .guide-story p, .example p, .formula p, .topic > p');
        blocks.forEach((block) => {
          const walker = document.createTreeWalker(block, NodeFilter.SHOW_TEXT);
          const nodes = [];
          while (walker.nextNode()) if (!walker.currentNode.parentElement.closest('a, code, button, h2, h3, h4, .term')) nodes.push(walker.currentNode);
          nodes.forEach((node) => {
            const parts = node.textContent.split(pattern);
            if (parts.length < 2) return;
            const fragment = document.createDocumentFragment();
            let changed = false;
            parts.forEach((part, i) => {
              if (i % 2 === 1 && !used.has(part.toLowerCase()) && used.size < 12) {
                used.add(part.toLowerCase());
                const button = Object.assign(document.createElement('button'), { type: 'button', className: 'term', textContent: part });
                button.setAttribute('aria-expanded', 'false');
                fragment.append(button);
                changed = true;
              } else fragment.append(part);
            });
            if (changed) node.replaceWith(fragment);
          });
        });
      });
    }).catch(() => {});
  }

  /* ---------- pick up where you stopped ---------- */
  if (courseId && chapters.length && !location.hash) {
    let saved;
    try { saved = JSON.parse(localStorage.getItem('leon-learn-progress') || '{}').courses?.[courseId]; } catch (_) {}
    const at = saved && chapters.findIndex((c) => c.id === saved.topic);
    if (at > 0) {
      const bar = document.createElement('div');
      bar.className = 'resume-bar';
      bar.innerHTML = `<span></span><a></a><button type="button"></button>`;
      bar.querySelector('span').textContent = chinese ? `上次读到第 ${at + 1} 章` : `You stopped at chapter ${at + 1}`;
      const link = bar.querySelector('a');
      link.href = `#${saved.topic}`;
      link.textContent = chinese ? '接着读' : 'Keep reading';
      const close = bar.querySelector('button');
      close.textContent = '×';
      close.setAttribute('aria-label', chinese ? '关闭' : 'Dismiss');
      close.addEventListener('click', () => bar.remove());
      link.addEventListener('click', () => bar.remove());
      document.querySelector('.course-hero')?.prepend(bar);
    }
  }

  /* ---------- phones: one chapter at a time, with a bar to move between them ---------- */
  if (courseId && chapters.length > 1 && window.matchMedia('(max-width: 760px)').matches) {
    const key = 'leon-learn-whole-page';
    let whole = false;
    try { whole = localStorage.getItem(key) === '1'; } catch (_) {}
    const words = chinese ? { of: (i, n) => `第 ${i} / ${n} 章`, start: '开始', contents: '目录', whole: '显示整门课', single: '一次一章', prev: '上一章', next: '下一章' } : { of: (i, n) => `Chapter ${i} of ${n}`, start: 'Start', contents: 'Contents', whole: 'Show whole course', single: 'One chapter at a time', prev: 'Previous chapter', next: 'Next chapter' };
    const bar = document.createElement('nav');
    bar.className = 'phone-bar';
    bar.setAttribute('aria-label', words.contents);
    bar.innerHTML = '<a class="pb-prev">‹</a><button type="button" class="pb-mid" aria-expanded="false"></button><a class="pb-next">›</a>';
    bar.querySelector('.pb-prev').setAttribute('aria-label', words.prev);
    bar.querySelector('.pb-next').setAttribute('aria-label', words.next);
    const sheet = document.createElement('div');
    sheet.className = 'phone-sheet';
    sheet.hidden = true;
    sheet.innerHTML = `<button type="button" class="pb-whole"></button><a href="#framework" class="pb-map"></a><ol></ol>`;
    sheet.querySelector('.pb-map').textContent = chinese ? '课程地图' : 'Course map';
    const ol = sheet.querySelector('ol');
    chapters.forEach((c) => { const li = document.createElement('li'); const a = document.createElement('a'); a.href = `#${c.id}`; a.textContent = c.querySelector('h2')?.textContent || c.id; li.append(a); ol.append(li); });
    document.body.append(sheet, bar);
    // the "show all answers" button lives in the course header, which chapter mode hides
    const answers = document.querySelector('[data-answers-toggle]');
    if (answers) { sheet.querySelector('.pb-map').after(answers); }
    const mid = bar.querySelector('.pb-mid');
    const setSheet = (open) => { sheet.hidden = !open; mid.setAttribute('aria-expanded', String(open)); };
    mid.addEventListener('click', () => setSheet(sheet.hidden));
    sheet.addEventListener('click', (event) => { if (event.target.closest('a')) setSheet(false); });
    const show = (scroll) => {
      document.body.classList.toggle('chapter-mode', !whole);
      sheet.querySelector('.pb-whole').textContent = whole ? words.single : words.whole;
      const target = location.hash.length > 1 ? document.getElementById(decodeURIComponent(location.hash.slice(1))) : null;
      let current = target?.closest?.('article.topic') || null;
      if (!current) {
        let saved;
        try { saved = JSON.parse(localStorage.getItem('leon-learn-progress') || '{}').courses?.[courseId]; } catch (_) {}
        current = !target && saved ? chapters.find((c) => c.id === saved.topic) || null : null;
      }
      const overview = !current;
      document.body.classList.toggle('chapter-overview', overview && !whole);
      chapters.forEach((c) => c.classList.toggle('is-open', c === current));
      const i = current ? chapters.indexOf(current) : -1;
      mid.textContent = current ? words.of(i + 1, chapters.length) : words.contents;
      const prev = bar.querySelector('.pb-prev');
      const next = bar.querySelector('.pb-next');
      prev.href = i > 0 ? `#${chapters[i - 1].id}` : '#framework';
      next.href = i < chapters.length - 1 ? `#${chapters[i + 1].id}` : '#references';
      ol.querySelectorAll('a').forEach((a, k) => a.classList.toggle('is-current', k === i));
      if (!whole && (scroll || current)) (target || current || document.body).scrollIntoView();
      requestAnimationFrame(fit);
      window.dispatchEvent(new Event('resize'));
    };
    sheet.querySelector('.pb-whole').addEventListener('click', () => { whole = !whole; try { localStorage.setItem(key, whole ? '1' : '0'); } catch (_) {} setSheet(false); show(false); });
    window.addEventListener('hashchange', () => show(true));
    show(!!location.hash);
  }

  let language;
  try { language = localStorage.getItem('guoliang-language'); } catch (_) {}
  if (language === 'zh') {
    document.querySelectorAll('[data-course-base]').forEach(link => {
      link.href = `${link.dataset.courseBase}.zh.html`;
    });
    document.querySelectorAll('[data-guide-base]').forEach(link => {
      link.href = `${link.dataset.guideBase}.zh.html`;
    });
  }
})();
