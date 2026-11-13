/* Homepage only: project filter, last-updated dates, and search across projects, courses and chapters. */
(() => {
  /* ---------- project filter ---------- */
  const filter = document.querySelector('.proj-filter');
  const grid = document.querySelector('.proj-grid');
  if (filter && grid) {
    filter.hidden = false;
    const cards = [...grid.querySelectorAll('.proj-card')];
    filter.addEventListener('click', (event) => {
      const button = event.target.closest('button[data-filter]');
      if (!button) return;
      const group = button.dataset.filter;
      filter.querySelectorAll('button').forEach((b) => b.setAttribute('aria-pressed', String(b === button)));
      cards.forEach((card) => { card.hidden = group !== 'all' && !card.dataset.groups.split(' ').includes(group); });
      grid.toggleAttribute('data-filtered', group !== 'all');
    });
  }

  /* ---------- last updated: one public GitHub API call, kept for an hour; silent if it fails ---------- */
  const stamps = [...document.querySelectorAll('.proj-updated[data-repo]')];
  const showDates = (dates) => stamps.forEach((el) => {
    const when = dates[el.dataset.repo];
    if (!when) return;
    const d = new Date(when);
    const text = d.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' });
    el.textContent = `Updated ${text}`;
    el.hidden = false;
  });
  const CACHE = 'leon-home-repo-dates';
  let cached;
  try { cached = JSON.parse(sessionStorage.getItem(CACHE)); } catch (_) { /* private mode */ }
  if (cached && Date.now() - cached.at < 36e5) showDates(cached.dates);
  else if (stamps.length) {
    fetch('https://api.github.com/users/leon1111-wgl/repos?per_page=100&sort=pushed', { headers: { Accept: 'application/vnd.github+json' } })
      .then((r) => (r.ok ? r.json() : Promise.reject(r.status)))
      .then((repos) => {
        const dates = Object.fromEntries(repos.map((r) => [r.name, r.pushed_at]));
        showDates(dates);
        try { sessionStorage.setItem(CACHE, JSON.stringify({ at: Date.now(), dates })); } catch (_) { /* private mode */ }
      })
      .catch(() => { /* the card reads fine without a date */ });
  }

  /* ---------- search ---------- */
  const opener = document.querySelector('[data-search-open]');
  if (!opener || typeof HTMLDialogElement === 'undefined') return;
  opener.hidden = false;
  const KIND = { project: 'Project', code: 'Code', research: 'Paper', course: 'Course', chapter: 'Chapter' };
  const RANK = { project: 0, research: 1, course: 2, chapter: 3, code: 4 };
  const dialog = document.createElement('dialog');
  dialog.className = 'search-dialog';
  dialog.setAttribute('aria-label', 'Search projects, courses and chapters');
  dialog.innerHTML = `<form method="dialog" class="search-box"><svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="6.5"/><path d="M16 16l4 4"/></svg><input type="search" role="combobox" aria-expanded="true" aria-controls="search-results" aria-autocomplete="list" autocomplete="off" spellcheck="false" placeholder="Search projects and chapters · 搜索项目和章节" aria-label="Search"><button type="submit" class="search-close" aria-label="Close search">Esc</button></form><ul id="search-results" role="listbox" aria-label="Results"></ul><p class="search-foot" aria-live="polite"></p>`;
  document.body.append(dialog);
  const input = dialog.querySelector('input');
  const list = dialog.querySelector('ul');
  const foot = dialog.querySelector('.search-foot');
  let items = null;
  let shown = [];
  let active = 0;
  const esc = (s) => String(s ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const cjk = (s) => /[一-鿿]/.test(s);
  const haystack = (x) => `${x.en} ${x.zh} ${x.sub || ''} ${x.kw || ''}`.toLowerCase();
  const score = (x, q) => {
    const en = x.en.toLowerCase();
    const zh = (x.zh || '').toLowerCase();
    if (en === q || zh === q) return 0;
    if (en.startsWith(q) || zh.startsWith(q)) return 1;
    if (en.includes(q) || zh.includes(q)) return 2;
    return 3;
  };
  /* chapters are ranked by what they teach (learn/data/search.json, assets/find.js) once that has loaded;
     projects, courses and the paper are matched by name as before and come first */
  let chapters = null;
  const loadChapters = () => {
    if (chapters || !window.LeonFind) return;
    chapters = 'loading';
    fetch('learn/data/search.json').then((r) => r.json()).then((index) => {
      chapters = index;
      // the project list may still be loading; it renders with the chapters once it arrives
      if (items && dialog.open && input.value.trim()) render();
    }, () => { chapters = null; });
  };
  const search = (raw) => {
    const q = raw.trim().toLowerCase();
    if (!q) return items.filter((x) => x.k === 'project' || x.k === 'research' || x.k === 'course');
    const words = q.split(/\s+/);
    const ranked = chapters && chapters !== 'loading';
    const named = items.filter((x) => (!ranked || x.k !== 'chapter') && (() => { const h = x.h ?? (x.h = haystack(x)); return words.every((w) => h.includes(w)); })())
      .sort((a, b) => score(a, q) - score(b, q) || RANK[a.k] - RANK[b.k]);
    if (!ranked) return named;
    const byId = new Map(items.filter((x) => x.k === 'chapter').map((x) => [x.id, x]));
    return [...named.filter((x) => x.k !== 'chapter'), ...window.LeonFind.search(chapters, q, 40).map((h) => byId.get(`${h.c}/${h.i}`)).filter(Boolean)];
  };
  const render = () => {
    const raw = input.value;
    const zh = cjk(raw);
    const all = search(raw);
    shown = all.slice(0, 40);
    active = Math.min(active, Math.max(shown.length - 1, 0));
    list.innerHTML = shown.map((x, i) => `<li role="option" id="sr-${i}" aria-selected="${i === active}"><a href="${esc((zh && x.urlZh) || x.url)}" tabindex="-1" style="--dot:${esc(x.color || 'var(--accent)')}"><span class="sr-kind">${KIND[x.k]}</span><span class="sr-main"><b${zh && x.zh ? ' lang="zh-CN"' : ''}>${esc(zh ? x.zh || x.en : x.en)}</b><small>${esc(x.k === 'project' && !zh ? x.sub : x.k === 'chapter' || x.k === 'course' ? (zh ? x.en : `${x.zh} · ${x.sub}`) : x.sub)}</small></span></a></li>`).join('');
    input.setAttribute('aria-activedescendant', shown.length ? `sr-${active}` : '');
    foot.textContent = raw.trim() ? (all.length ? `${all.length} result${all.length === 1 ? '' : 's'}${all.length > 40 ? ', showing the first 40' : ''}` : 'Nothing matches. Try a shorter word, or a Chinese or English term.') : 'Enter opens · ↑ ↓ moves · Esc closes';
  };
  const move = (by) => {
    if (!shown.length) return;
    active = (active + by + shown.length) % shown.length;
    list.querySelectorAll('li').forEach((li, i) => li.setAttribute('aria-selected', String(i === active)));
    input.setAttribute('aria-activedescendant', `sr-${active}`);
    list.children[active].scrollIntoView({ block: 'nearest' });
  };
  const open = async () => {
    if (dialog.open) return;
    dialog.showModal();
    input.focus();
    input.select();
    loadChapters();
    if (!items) {
      foot.textContent = 'Loading…';
      try {
        items = await fetch('assets/search-index.json').then((r) => r.json());
      } catch (_) {
        foot.textContent = 'Search could not load. The links on this page still work.';
        return;
      }
    }
    render();
  };
  opener.addEventListener('click', open);
  input.addEventListener('input', () => { active = 0; if (items) render(); });
  input.addEventListener('keydown', (event) => {
    // a search input swallows the first Esc to clear itself; here Esc always closes
    if (event.key === 'Escape') { event.preventDefault(); dialog.close(); }
    if (event.key === 'ArrowDown') { event.preventDefault(); move(1); }
    if (event.key === 'ArrowUp') { event.preventDefault(); move(-1); }
    if (event.key === 'Enter') {
      event.preventDefault();
      const link = list.children[active]?.querySelector('a');
      if (link) { dialog.close(); link.click(); }
    }
  });
  list.addEventListener('click', (event) => { if (event.target.closest('a')) dialog.close(); });
  dialog.addEventListener('click', (event) => { if (event.target === dialog) dialog.close(); });
  document.addEventListener('keydown', (event) => {
    const typing = /^(INPUT|TEXTAREA|SELECT)$/.test(event.target.tagName) || event.target.isContentEditable;
    if ((event.key === '/' && !typing) || ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k')) {
      event.preventDefault();
      open();
    }
  });
})();
