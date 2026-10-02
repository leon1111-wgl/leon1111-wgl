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
  button?.addEventListener('click', () => {
    const theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
    setTheme(theme);
    try { localStorage.setItem('guoliang-theme', theme); } catch (_) {}
  });
  const toc = document.querySelector('.toc details');
  if (toc && window.matchMedia('(max-width: 640px)').matches) toc.open = false;
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
        }).sort((a, b) => b.visible - a.visible).find(item => item.visible > 0)?.section;
      const target = new URL(link.href);
      target.hash = current?.id || window.location.hash;
      link.href = target.href;
    });
  });
  let language;
  try { language = localStorage.getItem('guoliang-language'); } catch (_) {}
  if (language === 'zh') {
    document.querySelectorAll('[data-guide-base]').forEach(link => {
      link.href = `${link.dataset.guideBase}.zh.html`;
    });
  }
})();
