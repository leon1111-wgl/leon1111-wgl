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
  const courseId = document.body.dataset.courseId;
  const chapters = [...document.querySelectorAll('article.topic[data-reading-id]')];
  if (courseId && chapters.length) {
    const tocLinks = new Map([...document.querySelectorAll('.toc ol a')].map(link => [link.getAttribute('href').slice(1), link]));
    let pending;
    const track = () => {
      let current = null;
      for (const chapter of chapters) {
        if (chapter.getBoundingClientRect().top <= 140) current = chapter; else break;
      }
      tocLinks.forEach((link, id) => link.classList.toggle('is-current', id === current?.id));
      if (!current) return;
      try {
        const saved = JSON.parse(localStorage.getItem('leon-learn-progress') || '{}');
        saved.courses = saved.courses || {};
        saved.courses[courseId] = {
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
