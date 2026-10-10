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
