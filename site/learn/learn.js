/* Learning hub: an intro page, then a five-view workspace (list, detail, route, cheatsheets, mine).
   Hash routes: #/ · #/courses · #/course/<id> · #/route · #/sheets · #/mine. No build step. */
(() => {
  const DATA = JSON.parse(document.getElementById('learn-data').textContent);
  const BY_ID = Object.fromEntries(DATA.courses.map((c) => [c.id, c]));
  const app = document.getElementById('app');
  const SITE = '../';

  /* ------------------------------------------------------------ storage (this browser only) */
  const store = {
    get(key, fallback) { try { const v = localStorage.getItem(key); return v === null ? fallback : JSON.parse(v); } catch (_) { return fallback; } },
    set(key, value) { try { localStorage.setItem(key, JSON.stringify(value)); } catch (_) { /* private mode */ } },
    remove(key) { try { localStorage.removeItem(key); } catch (_) { /* private mode */ } },
  };
  const langKey = 'guoliang-language'; // shared with the reading pages
  let lang = (() => { try { return localStorage.getItem(langKey) === 'en' ? 'en' : 'zh'; } catch (_) { return 'zh'; } })();
  const setLang = (l) => { lang = l; try { localStorage.setItem(langKey, l); } catch (_) { /* private mode */ } };
  const stars = () => store.get('leon-learn-stars', []);
  const recent = () => store.get('leon-learn-recent', []).filter((id) => BY_ID[id]);
  const progress = () => store.get('leon-learn-progress', { courses: {} });

  /* ------------------------------------------------------------ text */
  const T = {
    zh: {
      brand: 'Leon 学习', brandSub: '学习中心', enter: '进入学习',
      navHome: '首页', navCatalog: '课程', navHow: '怎么读', navFaq: '常见问题',
      list: '课程列表', detail: '课程详情', route: '学习路线', sheets: '速查表', mine: '我的学习',
      sList: '课程', sDetail: '详情', sRoute: '路线', sSheets: '速查', sMine: '我的',
      heroA: '从零学会编程', heroB: '中英双语',
      lead: '从第一行 Python 到算法、系统和人工智能。每章先讲一个小故事，再讲原理和公式，最后用能运行的代码验证。中文和英文随时切换。',
      notSure: '不知道从哪开始？', skip: '下次直接进入课程',
      chips: ['中英双语', '可运行代码', '一页速查表'],
      mapTitle: '学习地图', mapHint: '点一座小屋进入课程。沿着这条路走，就是推荐的学习顺序。', youAreHere: '你在这里', mapEnter: '进入课程',
      resume: '继续上次的阅读', resumeBtn: '接着读',
      statCourses: '门课程与学习路线', statChapters: '个章节', statPrograms: '份可运行代码', statSheets: '张一页速查表',
      catalogEyebrow: '课程', catalogTitle: '四个阶段，十一门课', catalogSub: '每门课都能单独读。第一次学编程，建议从「入门」开始。',
      howEyebrow: '怎么读', howTitle: '每一章都按同样的六步走', howSub: '先有直觉，再有严谨。读完一章，你能用自己的话把它讲清楚。', play: '播放', pause: '暂停', howPanel: '一章里有什么',
      howSteps: [
        ['故事', '从一个日常场景开始', '抽象概念先找一个熟悉的落脚点：排队、点外卖、整理书架。'],
        ['原理', '讲清楚为什么这样做', '解释背后的机制和前提，也说明类比在哪里不再成立。'],
        ['公式', '每个符号都解释', '公式逐项拆开读，不跳步，不默认你已经会。'],
        ['例子', '用具体数字算一遍', '拿一组小数据，一步一步算出结果，看规则怎样起作用。'],
        ['代码', '能直接运行的程序', '复制就能运行，并附上预期输出，方便你核对。'],
        ['自测', '一道新题检验自己', '换一个问题再想一遍，答案折叠在下面，想好了再看。'],
      ],
      howNotes: ['中文和英文章节一一对应', '专业术语首次出现都有解释', '每章末尾直接跳到下一章'],
      faqEyebrow: '常见问题', faqTitle: '开始之前',
      faq: [
        ['我完全没学过编程，从哪开始？', '从「Python 零基础实操」开始，第 0 单元会带你把第一段程序跑起来。之后读「AI 入门 8 讲」，补上向量、概率和梯度的直觉，再按学习路线往下走。'],
        ['中文版和英文版内容一样吗？', '五门课程和五条 AI 路线都有完整的中英文版本，章节一一对应，阅读时可以在右上角随时切换，会停在同一章。「Python 零基础实操」目前只有中文。'],
        ['需要安装什么？', 'Python 课程需要 Python 3.12 或更新版本；Java 课程需要 JDK 8 或更新版本；C 课程需要 gcc 或 clang。每门课开头都写了安装和运行步骤。'],
        ['速查表怎么用？', '学完一门课后用来复习。网页版的每一条都能点回对应章节；PDF 版是一页纸，适合打印（英文）。'],
        ['我的进度保存在哪里？', '收藏、最近浏览和上次读到的位置只保存在你自己的浏览器里，不会上传。换电脑或清除浏览器数据后会消失。'],
        ['这些是官方课程吗？', '不是。课程编号只表示内容对应的课程方向。这些是独立整理的学习笔记，不是官方教材，也不包含作业或考试材料。'],
      ],
      endTitle: '准备好了就开始', endSub: '从第一章开始，或者直接挑一门感兴趣的课。',
      listSub: (n, ch) => `${n} 门课程与学习路线 · 共 ${ch} 章`,
      all: '全部', search: '搜索课程或编号', colCourse: '课程', colChapters: '章节', colCode: '代码', colLang: '语言',
      chaptersUnit: '章', programsUnit: '份', bilingual: '中英双语', zhOnly: '仅中文', both: '中 · EN',
      read: '阅读', details: '详情', star: '收藏', unstar: '取消收藏', noMatch: '没有找到匹配的课程。',
      readTo: (n) => `读到第 ${n} 章`,
      facts: { chapters: '章节', programs: '可运行代码', problems: '推导例题', exercises: '练习', projects: '综合项目', language: '语言' },
      toc: '章节目录', chaptersCount: (n) => `${n} 章`,
      startRead: '从第 1 章开始', continueAt: '继续上次', otherLang: 'Read in English', otherLangOnly: '这门课只有中文版',
      sheetTitle: '速查表', sheetWeb: '网页版', sheetPdf: 'PDF（英文）', sheetSection: '复习速查',
      notesMd: '下载讲义（Markdown）', notesZip: '下载完整学习包（ZIP）',
      before: '开始前需要了解', outcomes: '学完你会',
      routeSub: '按这个顺序读，每一步都建立在上一步之上。已经会的部分可以跳过。', stage: '阶段',
      sheetsSub: '学完一门课后用来复习。网页版的每一条都能点回对应章节。',
      collection: '五门课速查表合集', collectionNote: 'PDF · 5 页 · 英文 · 适合打印', download: '下载',
      reviewNote: '每章一条要点，点回原文', pythonSheet: '八周复习路线与综合自测',
      mineSub: '收藏、最近浏览和上次读到的位置，只保存在这个浏览器里。',
      last: '上次读到', starred: '收藏的课程', recentT: '最近浏览', clear: '清除记录',
      emptyLast: '还没有阅读记录。打开任意一章，这里会记住你读到哪里。', emptyStars: '在课程列表点 ☆ 就能收藏。', emptyRecent: '看过详情的课程会出现在这里。',
      footNote: '独立整理的学习笔记，不是官方课程材料 · 进度只保存在本机浏览器', home: '个人主页',
      notFound: '没有找到这个页面。', back: '回到课程列表', lang: '阅读语言',
    },
    en: {
      brand: 'Leon Learn', brandSub: 'Learning hub', enter: 'Start learning',
      navHome: 'Home', navCatalog: 'Courses', navHow: 'How it works', navFaq: 'FAQ',
      list: 'Courses', detail: 'Course', route: 'Learning route', sheets: 'Cheatsheets', mine: 'My learning',
      sList: 'Courses', sDetail: 'Course', sRoute: 'Route', sSheets: 'Sheets', sMine: 'Mine',
      heroA: 'Learn to code from zero', heroB: 'Chinese & English',
      lead: 'From your first line of Python to algorithms, systems and AI. Each chapter starts with a short story, explains the idea and the formula, and ends with code you can run. Switch between Chinese and English at any time.',
      notSure: 'Not sure where to start?', skip: 'Skip this page next time',
      chips: ['Chinese and English', 'Runnable code', 'One-page cheatsheets'],
      mapTitle: 'Learning map', mapHint: 'Tap a house to open its course. The road follows the suggested order.', youAreHere: 'You are here', mapEnter: 'Open course',
      resume: 'Pick up where you left off', resumeBtn: 'Keep reading',
      statCourses: 'courses and guides', statChapters: 'chapters', statPrograms: 'runnable programs', statSheets: 'one-page cheatsheets',
      catalogEyebrow: 'COURSES', catalogTitle: 'Four stages, eleven courses', catalogSub: 'Every course stands on its own. New to programming? Begin with Get started.',
      howEyebrow: 'HOW IT WORKS', howTitle: 'Every chapter follows the same six steps', howSub: 'Intuition first, then rigour. After a chapter you can explain the idea in your own words.', play: 'Play', pause: 'Pause', howPanel: 'Inside a chapter',
      howSteps: [
        ['Story', 'Begin with an everyday scene', 'An abstract idea first gets a familiar place to stand: a queue, a food order, a bookshelf.'],
        ['Principle', 'Why it works', 'The mechanism and its assumptions, and where the analogy stops.'],
        ['Formula', 'Every symbol explained', 'Formulas are read term by term. No skipped steps, nothing assumed.'],
        ['Example', 'Work it with real numbers', 'Take a small input and compute the result step by step.'],
        ['Code', 'Programs you can run', 'Copy, run, and compare with the expected output shown underneath.'],
        ['Check', 'Test yourself on a new question', 'A fresh problem with a folded answer. Think first, then open it.'],
      ],
      howNotes: ['Chinese and English chapters match one to one', 'Every term is defined when it first appears', 'Each chapter links straight to the next'],
      faqEyebrow: 'FAQ', faqTitle: 'Before you start',
      faq: [
        ['I have never programmed. Where do I start?', 'Start with Python: Zero to Practice; unit 0 gets your first program running. Then read Start Here, eight short lessons on vectors, probability and gradients, and follow the learning route from there.'],
        ['Are the Chinese and English editions the same?', 'All five courses and five AI guides have complete Chinese and English editions with matching chapters. Switch at the top right while reading and you stay on the same chapter. The Python handbook is in Chinese only.'],
        ['What do I need to install?', 'Python 3.12 or newer for the Python material, JDK 8 or newer for Java, and gcc or clang for C. Each course opens with setup and run steps.'],
        ['How do I use the cheatsheets?', 'Use them to review after a course. Every item on the web version links back to its chapter; the PDF fits on one printable page (English).'],
        ['Where is my progress saved?', 'Stars, recently viewed courses and your last reading position stay in your own browser. Nothing is uploaded. They disappear if you change computers or clear browser data.'],
        ['Are these official courses?', 'No. A course code only shows which subject the material follows. These are independent study notes, not official course material, and they contain no assignments or exams.'],
      ],
      endTitle: 'Ready when you are', endSub: 'Begin at chapter one, or pick any course that interests you.',
      listSub: (n, ch) => `${n} courses and guides · ${ch} chapters`,
      all: 'All', search: 'Search by title or code', colCourse: 'Course', colChapters: 'Chapters', colCode: 'Code', colLang: 'Language',
      chaptersUnit: 'chapters', programsUnit: 'programs', bilingual: 'Chinese + English', zhOnly: 'Chinese only', both: '中 · EN',
      read: 'Read', details: 'Details', star: 'Star', unstar: 'Remove star', noMatch: 'No course matches.',
      readTo: (n) => `At chapter ${n}`,
      facts: { chapters: 'Chapters', programs: 'Runnable programs', problems: 'Worked problems', exercises: 'Exercises', projects: 'Projects', language: 'Language' },
      toc: 'Chapters', chaptersCount: (n) => `${n} chapters`,
      startRead: 'Start at chapter 1', continueAt: 'Continue', otherLang: '用中文阅读', otherLangOnly: 'This course is in Chinese only',
      sheetTitle: 'Cheatsheet', sheetWeb: 'Web', sheetPdf: 'PDF (English)', sheetSection: 'Review',
      notesMd: 'Download notes (Markdown)', notesZip: 'Download the learning kit (ZIP)',
      before: 'Before you start', outcomes: 'You will be able to',
      routeSub: 'Read in this order; each step builds on the one before. Skip whatever you already know.', stage: 'Stage',
      sheetsSub: 'Use these to review after a course. Every item on the web version links back to its chapter.',
      collection: 'All five course cheatsheets', collectionNote: 'PDF · 5 pages · English · ready to print', download: 'Download',
      reviewNote: 'One key point per chapter, linked to the text', pythonSheet: 'Eight-week review route and self-tests',
      mineSub: 'Stars, recent courses and your last reading position, kept in this browser only.',
      last: 'Last read', starred: 'Starred', recentT: 'Recently viewed', clear: 'Clear history',
      emptyLast: 'Nothing read yet. Open any chapter and this remembers where you stopped.', emptyStars: 'Tap ☆ in the course list to star a course.', emptyRecent: 'Courses you open appear here.',
      footNote: 'Independent study notes, not official course material · Progress stays in this browser', home: 'Homepage',
      notFound: 'This page does not exist.', back: 'Back to courses', lang: 'Reading language',
    },
  };
  const t = (key) => T[lang][key];
  const L = (obj) => (obj && typeof obj === 'object' ? (obj[lang] ?? obj.zh ?? obj.en) : obj);
  const other = (obj) => (obj && typeof obj === 'object' ? obj[lang === 'zh' ? 'en' : 'zh'] : '');
  const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (ch) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[ch]));
  const pad = (n) => String(n).padStart(2, '0');

  /* ------------------------------------------------------------ icons */
  const P = {
    python: '<path d="M4 5h16v14H4z"/><path d="M7.5 9.5l3 2.5-3 2.5M12.5 15h4"/>',
    start: '<path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M5.6 18.4l2.1-2.1M16.3 7.7l2.1-2.1"/><circle cx="12" cy="12" r="2.5"/>',
    objects: '<path d="M12 3l8 4.5v9L12 21l-8-4.5v-9z"/><path d="M4 7.5l8 4.5 8-4.5M12 12v9"/>',
    graph: '<circle cx="6" cy="6" r="2.2"/><circle cx="18" cy="7" r="2.2"/><circle cx="7" cy="18" r="2.2"/><circle cx="17.5" cy="17.5" r="2.2"/><path d="M8 6.5l8 .3M6.5 8.2l.4 7.6M16.6 9l.8 6.3M9.2 17.9l6.1-.3"/>',
    chip: '<rect x="7" y="7" width="10" height="10" rx="1.5"/><path d="M10 3v4M14 3v4M10 17v4M14 17v4M3 10h4M3 14h4M17 10h4M17 14h4"/>',
    automaton: '<circle cx="6.5" cy="12" r="3.2"/><circle cx="17.5" cy="12" r="3.2"/><circle cx="17.5" cy="12" r="1.6"/><path d="M9.7 11h4.6M12.6 9.4l1.7 1.6-1.7 1.6M5 8.5C5.5 5 8 4 9.5 6"/>',
    search: '<circle cx="12" cy="5" r="2"/><circle cx="6" cy="13" r="2"/><circle cx="18" cy="13" r="2"/><circle cx="14" cy="20" r="1.6"/><path d="M10.8 6.6L7.2 11.4M13.2 6.6l3.6 4.8M17.2 14.9l-2.4 3.6"/>',
    scatter: '<path d="M4 20h16M4 20V4"/><path d="M6.5 17L19 7"/><circle cx="8" cy="12.5" r="1"/><circle cx="11" cy="15" r="1"/><circle cx="13" cy="9.5" r="1"/><circle cx="16.5" cy="11" r="1"/>',
    layers: '<path d="M12 4l9 4.5-9 4.5-9-4.5z"/><path d="M3 12.5l9 4.5 9-4.5M3 16.5l9 4.5 9-4.5"/>',
    eye: '<path d="M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12z"/><circle cx="12" cy="12" r="3"/>',
    media: '<rect x="3" y="4" width="11" height="9" rx="1.5"/><path d="M3 11l3-3 3 3 2-2 3 3"/><path d="M17 6h4M17 10h4M8 17h13M8 20.5h9"/>',
    find: '<circle cx="11" cy="11" r="6.5"/><path d="M16 16l4 4"/>',
    grid: '<rect x="4" y="4" width="7" height="7" rx="1.5"/><rect x="13" y="4" width="7" height="7" rx="1.5"/><rect x="4" y="13" width="7" height="7" rx="1.5"/><rect x="13" y="13" width="7" height="7" rx="1.5"/>',
    book: '<path d="M12 6.5C10 5 7 4.6 4 5v13c3-.4 6 0 8 1.5 2-1.5 5-1.9 8-1.5V5c-3-.4-6 0-8 1.5zM12 6.5v13"/>',
    route: '<circle cx="6" cy="18" r="2.2"/><circle cx="18" cy="6" r="2.2"/><path d="M8.2 18H15a3 3 0 0 0 0-6H9a3 3 0 0 1 0-6h6.8"/>',
    sheet: '<path d="M7 3h7l4 4v14H7z"/><path d="M14 3v4h4M10 11h5M10 14.5h5M10 18h3"/>',
    user: '<circle cx="12" cy="8.5" r="3.5"/><path d="M5 20c.8-3.6 3.6-5.5 7-5.5s6.2 1.9 7 5.5"/>',
    star: '<path d="M12 3.8l2.5 5.1 5.6.8-4 3.9 1 5.6-5.1-2.7-5 2.7.9-5.6-4-3.9 5.6-.8z"/>',
    globe: '<circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17M12 3.5c2.4 2.3 3.6 5.2 3.6 8.5s-1.2 6.2-3.6 8.5c-2.4-2.3-3.6-5.2-3.6-8.5S9.6 5.8 12 3.5z"/>',
    arrow: '<path d="M5 12h14M13 6l6 6-6 6"/>',
    down: '<path d="M12 4v12M6.5 11l5.5 5.5 5.5-5.5M5 20h14"/>',
    check: '<circle cx="12" cy="12" r="8.5"/><path d="M8.2 12.2l2.6 2.6 5-5.3"/>',
    plus: '<path d="M12 5v14M5 12h14"/>',
    play: '<path d="M8 5.5v13l10-6.5z"/>', pause: '<path d="M8.5 5.5v13M15.5 5.5v13"/>',
    story: '<path d="M5 5h14v10H9l-4 4z"/>', principle: '<circle cx="12" cy="10" r="5.5"/><path d="M10 19h4M10.5 15.5v3.5M13.5 15.5v3.5"/>',
    formula: '<path d="M5 6h7l-5 6 5 6H5M15 9l5 6M20 9l-5 6"/>', example: '<rect x="4" y="4" width="16" height="16" rx="2"/><path d="M8 9h3M9.5 7.5v3M13 9h3M8 15.5l3-1.5M8 14l3 1.5M13 14.5h3M13 16h3"/>',
    code: '<path d="M9 7l-5 5 5 5M15 7l5 5-5 5"/>', quiz: '<circle cx="12" cy="12" r="8.5"/><path d="M9.6 9.5a2.5 2.5 0 1 1 3.3 2.4c-.6.3-.9.8-.9 1.4v.5M12 16.8v.2"/>',
  };
  const icon = (name) => `<svg class="i" viewBox="0 0 24 24" aria-hidden="true">${P[name] || ''}</svg>`;
  const HOW_ICONS = ['story', 'principle', 'formula', 'example', 'code', 'quiz'];

  /* ------------------------------------------------------------ links */
  const readLang = (c) => (c.read[lang] ? lang : c.langs[0]);
  const readUrl = (c, chapter, l = readLang(c)) => SITE + c.read[l] + (chapter ? '#' + chapter : '');
  const courseProgress = (c) => progress().courses?.[c.id];
  const chapterIndex = (c, id) => c.chapters.findIndex((ch) => ch.id === id);
  const href = { intro: '#/', list: '#/courses', course: (id) => `#/course/${id}`, route: '#/route', sheets: '#/sheets', mine: '#/mine' };

  /* ------------------------------------------------------------ pieces */
  const langToggle = () => `<div class="lang" role="group" aria-label="${t('lang')}">${icon('globe')}<div class="segmented">` +
    ['zh', 'en'].map((l) => `<button type="button" data-lang="${l}" aria-pressed="${lang === l}">${l === 'zh' ? '中文' : 'EN'}</button>`).join('') + '</div></div>';
  const brand = (to) => `<a class="brand" href="${to}"><span class="mark">LW</span>${t('brand')}<small>${t('brandSub')}</small></a>`;
  const langTag = (c) => (c.langs.length > 1 ? `<span class="tag">${t('bilingual')}</span>` : `<span class="tag">${t('zhOnly')}</span>`);
  const levelTag = (c) => `<span class="tag accent">${esc(L(DATA.levels[c.level]))}</span>`;
  const tile = (c, big = false) => `<span class="icon-tile${big ? ' lg' : ''}" style="--accent:${c.color}">${icon(c.icon)}</span>`;
  const footer = () => `<footer class="foot"><span>${t('footNote')}</span><span><a href="${SITE}index.html">${t('home')} ↗</a> · © 2026 Leon Wang</span></footer>`;

  /* ------------------------------------------------------------ intro */
  function introView() {
    const p = progress();
    const last = p.latest && BY_ID[p.latest] && p.courses?.[p.latest];
    const resume = last ? `<a class="resume reveal d2" href="${SITE + esc(last.url)}" style="--accent:${BY_ID[p.latest].color}"><small>${t('resume')}</small><b>${esc(BY_ID[p.latest].code)} · ${esc(last.title)}</b>${icon('arrow')}</a>` : '';
    const here = last ? p.latest : 'python';
    const legend = Object.keys(DATA.tracks).map((k) => `<span style="--d:var(--t-${k})"><i></i>${esc(L(DATA.tracks[k]))}</span>`).join('');
    const tot = DATA.totals;
    const tracks = DATA.route.map((r) => `<article class="panel track" data-track="${r.track}"><div><h3>${esc(L(DATA.tracks[r.track]))}</h3><p>${esc(L(r.note))}</p></div><ul>` +
      r.courses.map((id) => { const c = BY_ID[id]; return `<li><a href="${href.course(id)}" style="--accent:${c.color}"><span class="code">${esc(c.code)}</span><span>${esc(L(c.title))}</span></a></li>`; }).join('') + '</ul></article>').join('');
    const steps = t('howSteps');
    const faq = t('faq').map(([q, a]) => `<details><summary>${esc(q)}${icon('plus')}</summary><p>${esc(a)}</p></details>`).join('');
    return `<div class="intro-page">
      <header class="intro-bar">${brand(href.intro)}
        <nav class="pill-nav" aria-label="${t('navHome')}"><span class="slider" aria-hidden="true"></span>
          ${[['hero', 'navHome'], ['catalog', 'navCatalog'], ['how', 'navHow'], ['faq', 'navFaq']].map(([id, k]) => `<button type="button" data-scroll="${id}">${t(k)}</button>`).join('')}
        </nav>
        <div class="intro-actions">${langToggle()}<a class="btn primary" href="${href.list}">${t('enter')}</a></div>
      </header>
      <section class="hero" id="hero">
        <div>
          <h1 class="reveal">${t('heroA')}<br><span class="hl">${t('heroB')}</span></h1>
          <p class="lead reveal d1">${t('lead')}</p>
          <div class="cta reveal d2"><a class="btn primary lg" href="${href.list}">${t('enter')} ${icon('arrow')}</a><a class="btn ghost lg" href="${href.route}">${t('notSure')}</a></div>
          ${resume}
          <label class="skip-intro reveal d2"><input type="checkbox" data-skip ${store.get('leon-learn-skip-intro', false) ? 'checked' : ''}>${t('skip')}</label>
          <div class="chips reveal d3">${t('chips').map((c) => `<span>${icon('check')}${c}</span>`).join('')}</div>
        </div>
        <aside class="panel map-card reveal d2">
          <div class="panel-head"><h2>${t('mapTitle')}</h2><div class="legend">${legend}</div></div>
          ${mapSvg(here)}
          <div class="map-caption" data-caption aria-live="polite">${icon('route')}<span>${t('mapHint')}</span></div>
        </aside>
      </section>
      <div class="stats">
        <div><b>${tot.courses}</b><span>${t('statCourses')}</span></div><div><b>${tot.chapters}</b><span>${t('statChapters')}</span></div>
        <div><b>${tot.programs}</b><span>${t('statPrograms')}</span></div><div><b>${tot.sheets}</b><span>${t('statSheets')}</span></div>
      </div>
      <section class="intro-section" id="catalog"><header><div><span class="eyebrow">${t('catalogEyebrow')}</span><h2>${t('catalogTitle')}</h2></div><p>${t('catalogSub')}</p></header><div class="tracks">${tracks}</div></section>
      <section class="intro-section" id="how"><header><div><span class="eyebrow">${t('howEyebrow')}</span><h2>${t('howTitle')}</h2></div><p>${t('howSub')}</p></header>
        <div class="panel how"><div class="panel-head"><h2>${t('howPanel')}</h2><button type="button" class="btn ghost sm" data-play>${icon('pause')}<span>${t('pause')}</span></button></div>
          <div class="how-tabs" role="tablist">${steps.map((s, i) => `<button type="button" role="tab" id="how-tab-${i}" aria-controls="how-panel" data-step="${i}" aria-selected="${i === 0}"><span class="icon-tile">${icon(HOW_ICONS[i])}</span>${esc(s[0])}</button>`).join('')}</div>
          <div class="how-card" id="how-panel" role="tabpanel" aria-labelledby="how-tab-0" aria-live="polite"></div>
          <div class="how-notes">${t('howNotes').map((n) => `<span>${icon('check')}${esc(n)}</span>`).join('')}</div>
        </div>
      </section>
      <section class="intro-section" id="faq"><header><div><span class="eyebrow">${t('faqEyebrow')}</span><h2>${t('faqTitle')}</h2></div></header><div class="faq">${faq}</div></section>
      <div class="intro-end"><div><h2>${t('endTitle')}</h2><p>${t('endSub')}</p></div><a class="btn primary lg" href="${href.list}">${t('enter')} ${icon('arrow')}</a></div>
      ${footer()}
    </div>`;
  }

  let timers = [];
  let observer;
  function wireIntro() {
    const steps = t('howSteps');
    const card = app.querySelector('.how-card');
    const tabs = [...app.querySelectorAll('[data-step]')];
    let current = 0;
    let playing = !matchMedia('(prefers-reduced-motion: reduce)').matches;
    const show = (i) => {
      current = i;
      tabs.forEach((b, j) => b.setAttribute('aria-selected', String(i === j)));
      card.setAttribute('aria-labelledby', `how-tab-${i}`);
      const s = steps[i];
      card.innerHTML = `<span class="icon-tile lg">${icon(HOW_ICONS[i])}</span><div><small>${lang === 'zh' ? `第 ${i + 1} / 6 步` : `Step ${i + 1} of 6`}</small><h3>${esc(s[1])}</h3><p>${esc(s[2])}</p></div>`;
    };
    const play = app.querySelector('[data-play]');
    const setPlaying = (on) => {
      playing = on;
      play.innerHTML = `${icon(on ? 'pause' : 'play')}<span>${t(on ? 'pause' : 'play')}</span>`;
    };
    tabs.forEach((b) => b.addEventListener('click', () => { show(Number(b.dataset.step)); setPlaying(false); }));
    play.addEventListener('click', () => setPlaying(!playing));
    setPlaying(playing);
    show(0);
    timers.push(setInterval(() => { if (playing && !document.hidden) show((current + 1) % steps.length); }, 3800));

    const caption = app.querySelector('[data-caption]');
    const idle = caption.innerHTML;
    app.querySelectorAll('[data-house]').forEach((house) => {
      const c = BY_ID[house.dataset.house];
      const show = () => { caption.style.setProperty('--accent', c.color); caption.innerHTML = `<span class="dot"></span><span><b>${esc(c.code)} · ${esc(L(c.title))}</b><em>${c.stats.chapters} ${t('chaptersUnit')} · ${esc(L(DATA.tracks[c.track]))} · ${c.langs.length > 1 ? t('bilingual') : t('zhOnly')}</em></span><a class="btn light sm" href="${href.course(c.id)}">${t('mapEnter')} ${icon('arrow')}</a>`; };
      house.addEventListener('mouseenter', show);
      house.addEventListener('focus', show);
    });
    app.querySelector('.map').addEventListener('mouseleave', () => { caption.style.removeProperty('--accent'); caption.innerHTML = idle; });
    app.querySelector('[data-skip]').addEventListener('change', (e) => store.set('leon-learn-skip-intro', e.target.checked));

    // the pill under the intro navigation follows the section in view
    const nav = app.querySelector('.pill-nav');
    const slider = nav.querySelector('.slider');
    const buttons = [...nav.querySelectorAll('[data-scroll]')];
    const mark = (id) => {
      const b = buttons.find((x) => x.dataset.scroll === id) || buttons[0];
      buttons.forEach((x) => x.setAttribute('aria-current', String(x === b)));
      slider.style.width = `${b.offsetWidth}px`;
      slider.style.transform = `translateX(${b.offsetLeft}px)`;
    };
    buttons.forEach((b) => b.addEventListener('click', () => {
      const target = document.getElementById(b.dataset.scroll);
      window.scrollTo({ top: b.dataset.scroll === 'hero' ? 0 : target.getBoundingClientRect().top + window.scrollY - 90, behavior: 'smooth' });
    }));
    mark('hero');
    const sections = buttons.map((b) => document.getElementById(b.dataset.scroll));
    const onScroll = () => {
      const y = window.scrollY + window.innerHeight * 0.35;
      let id = 'hero';
      sections.forEach((s) => { if (s.offsetTop <= y) id = s.id; });
      if (window.innerHeight + window.scrollY >= document.body.scrollHeight - 4) id = sections[sections.length - 1].id;
      mark(id);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);
    observer = () => { window.removeEventListener('scroll', onScroll); window.removeEventListener('resize', onScroll); };
  }

  /* ------------------------------------------------------------ workspace frame */
  const NAV = [['list', 'grid', 'list', 'sList'], ['detail', 'book', 'detail', 'sDetail'], ['route', 'route', 'route', 'sRoute'], ['sheets', 'sheet', 'sheets', 'sSheets'], ['mine', 'user', 'mine', 'sMine']];
  function frame(active, body) {
    const lastCourse = recent()[0] || DATA.courses[0].id;
    const to = { list: href.list, detail: href.course(lastCourse), route: href.route, sheets: href.sheets, mine: href.mine };
    return `<header class="topbar">${brand(href.intro)}
      <nav class="main-nav" aria-label="${t('brand')}">${NAV.map(([key, ic, long, short]) => `<a class="nav-item${active === key ? ' active' : ''}" href="${to[key]}"${active === key ? ' aria-current="page"' : ''}>${icon(ic)}<span class="nav-long">${t(long)}</span><span class="nav-short">${t(short)}</span></a>`).join('')}</nav>
      <div class="top-actions"><a class="top-link" href="${SITE}index.html">${t('home')} ↗</a>${langToggle()}</div>
    </header><main class="shell">${body}</main>${footer()}`;
  }

  /* ------------------------------------------------------------ list */
  const ui = { filter: 'all', q: '' };
  const matches = (c) => {
    if (ui.filter !== 'all' && c.track !== ui.filter) return false;
    const q = ui.q.trim().toLowerCase();
    if (!q) return true;
    return [c.code, c.title.zh, c.title.en, c.subtitle.zh, c.subtitle.en].some((s) => String(s || '').toLowerCase().includes(q));
  };
  function rowsHtml() {
    const s = stars();
    const list = DATA.courses.filter(matches);
    if (!list.length) return `<tr><td colspan="6"><div class="empty">${t('noMatch')}</div></td></tr>`;
    return list.map((c) => {
      const pr = courseProgress(c);
      const at = pr ? chapterIndex(c, pr.topic) : -1;
      const prog = at >= 0 ? `<small>${t('readTo')(at + 1)}</small><span class="progress-line"><i style="width:${Math.round(((at + 1) / c.chapters.length) * 100)}%"></i></span>` : `<small>${t('chaptersUnit')}</small>`;
      const starred = s.includes(c.id);
      return `<tr style="--accent:${c.color}">
        <td class="star-cell"><button type="button" class="star" data-star="${c.id}" aria-pressed="${starred}" aria-label="${starred ? t('unstar') : t('star')}">${icon('star')}</button></td>
        <td><div class="cell-course">${tile(c)}<div class="t"><b><span class="code">${esc(c.code)}</span>&nbsp; <a href="${href.course(c.id)}">${esc(L(c.title))}</a></b><span class="alt">${esc(other(c.title) || L(c.subtitle))}</span><span class="tags">${levelTag(c)}${langTag(c)}</span></div></div></td>
        <td class="n">${c.stats.chapters}${prog}</td>
        <td class="n hide-sm">${c.stats.programs || 0}<small>${t('programsUnit')}</small></td>
        <td class="hide-sm"><span class="tag">${c.langs.length > 1 ? t('both') : t('zhOnly')}</span></td>
        <td><div class="row-actions"><a class="btn ghost sm" href="${href.course(c.id)}">${t('details')}</a><a class="btn light sm" href="${pr ? SITE + esc(pr.url) : readUrl(c)}">${t('read')}</a></div></td>
      </tr>`;
    }).join('');
  }
  function listView() {
    const filters = [['all', t('all')], ...Object.keys(DATA.tracks).map((k) => [k, L(DATA.tracks[k])])];
    return frame('list', `<div class="page-head"><div><h1>${t('list')}</h1><p>${t('listSub')(DATA.totals.courses, DATA.totals.chapters)}</p></div></div>
      <section class="panel reveal">
        <div class="toolbar"><div class="filters" role="group">${filters.map(([k, label]) => `<button type="button" data-filter="${k}" aria-pressed="${ui.filter === k}">${esc(label)}</button>`).join('')}</div>
          <label class="search">${icon('find')}<span class="sr-only">${t('search')}</span><input type="search" data-q value="${esc(ui.q)}" placeholder="${t('search')}"></label></div>
        <table class="course-table"><thead><tr><th></th><th>${t('colCourse')}</th><th>${t('colChapters')}</th><th class="hide-sm">${t('colCode')}</th><th class="hide-sm">${t('colLang')}</th><th></th></tr></thead><tbody>${rowsHtml()}</tbody></table>
      </section>`);
  }
  function wireList() {
    app.querySelectorAll('[data-filter]').forEach((b) => b.addEventListener('click', () => {
      ui.filter = b.dataset.filter;
      app.querySelectorAll('[data-filter]').forEach((x) => x.setAttribute('aria-pressed', String(x === b)));
      app.querySelector('tbody').innerHTML = rowsHtml();
    }));
    app.querySelector('[data-q]').addEventListener('input', (e) => { ui.q = e.target.value; app.querySelector('tbody').innerHTML = rowsHtml(); });
  }

  /* chapters per stage, drawn as one segmented bar */
  const stageBar = (c) => `<div class="stage-bar" aria-hidden="true">${c.stages.map((s, i) => `<span style="flex:${s.chapters.length};--o:${0.35 + (0.65 * (i + 1)) / c.stages.length}"><i></i><b>${pad(i + 1)} · ${esc(L(s.title))}</b><em>${t('chaptersCount')(s.chapters.length)}</em></span>`).join('')}</div>`;

  /* ------------------------------------------------------------ the learning map */
  // Each course is a house (its place comes with the catalogue); the road visits them in the suggested order.
  const ORDER = DATA.route.flatMap((r) => r.courses).filter((id) => BY_ID[id]?.map);
  const smooth = (pts) => {
    let d = `M${pts[0][0]} ${pts[0][1]}`;
    for (let i = 0; i < pts.length - 1; i += 1) {
      const p0 = pts[i - 1] || pts[i]; const p1 = pts[i]; const p2 = pts[i + 1]; const p3 = pts[i + 2] || p2;
      const c1 = [p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6];
      const c2 = [p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6];
      d += ` C${c1[0].toFixed(1)} ${c1[1].toFixed(1)} ${c2[0].toFixed(1)} ${c2[1].toFixed(1)} ${p2[0]} ${p2[1]}`;
    }
    return d;
  };
  const textWidth = (s, size) => [...s].reduce((w, ch) => w + (/[\u2E80-\uFFFF]/.test(ch) ? size : size * 0.58), 0);
  function mapSvg(here) {
    const road = smooth(ORDER.map((id) => BY_ID[id].map));
    const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
    const district = (track, d, x, y) => `<path class="district" d="${d}" style="--d:var(--t-${track})"/><text class="district-name" x="${x}" y="${y}" style="--d:var(--t-${track})">${esc(L(DATA.tracks[track]))}</text>`;
    const tree = (x, y, r = 6) => `<g class="tree"><circle cx="${x}" cy="${y}" r="${r}"/><circle cx="${x + r * 0.9}" cy="${y + 2}" r="${r * 0.75}"/></g>`;
    const houses = ORDER.map((id, i) => {
      const c = BY_ID[id]; const [x, y] = c.map;
      const name = L(c.short); const w = Math.max(textWidth(name, 11.5), textWidth(c.code, 9)) + 18;
      return `<a class="house${id === here ? ' is-here' : ''}" href="${href.course(id)}" data-house="${id}" style="--c:${c.color}" transform="translate(${x} ${y})">
        <title>${esc(c.code)} · ${esc(L(c.title))}</title>
        <ellipse class="shadow" cx="0" cy="3" rx="19" ry="4.5"/>
        <g class="body"><rect class="wall" x="-12" y="-14" width="24" height="17" rx="2.5"/><path class="roof" d="M-16 -12.5 L0 -27 L16 -12.5 Z"/>
          <rect class="win" x="-9" y="-9.5" width="4.5" height="4.5" rx="1"/><rect class="win" x="4.5" y="-9.5" width="4.5" height="4.5" rx="1"/><rect class="door" x="-2.8" y="-6" width="5.6" height="9" rx="1.2"/>
          <text class="step" x="0" y="-15.5">${i + 1}</text></g>
        <g class="tag" transform="translate(0 11)"><rect x="${(-w / 2).toFixed(1)}" y="0" width="${w.toFixed(1)}" height="31" rx="8"/><text class="tn" x="0" y="13.5">${esc(name)}</text><text class="tc" x="0" y="25">${esc(c.code)}</text></g>
      </a>`;
    }).join('');
    const [hx, hy] = (BY_ID[here]?.map || BY_ID[ORDER[0]].map);
    return `<svg class="map" viewBox="0 0 640 470" role="group" aria-label="${t('mapTitle')}">
      <defs>
        <pattern id="topo" width="44" height="44" patternUnits="userSpaceOnUse"><path d="M0 22c11-7 22 7 33 0s11-7 11-7" fill="none" stroke="rgb(255 255 255 / 4%)"/></pattern>
        <radialGradient id="glowHere"><stop stop-color="#fff" stop-opacity=".5"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
      </defs>
      <rect width="640" height="470" fill="url(#topo)"/>
      ${district('core', 'M18 38C80 16 206 26 262 68c30 50 22 170-6 230-74-8-160 0-238 22Z', 34, 62)}
      ${district('systems', 'M276 26c70-20 196-10 246 32 22 50 4 132-48 152-74 12-152-6-188-48-10-48-12-90-10-136Z', 292, 50)}
      ${district('ai', 'M302 230c82-16 186-30 320-20v252H300c-16-82-14-170 2-232Z', 352, 454)}
      ${district('start', 'M18 468V334c46-30 140-40 234-12 40 22 50 100 22 146Z', 206, 456)}
      <path class="river" d="M250 0C232 80 304 140 282 214c-20 76 44 130 20 256"/>
      <path class="river-glint" d="M250 0C232 80 304 140 282 214c-20 76 44 130 20 256"/>
      <g class="hills"><path d="M356 72l20-34 20 34Z"/><path d="M384 72l24-40 24 40Z"/><path d="M500 92l20-32 20 32Z"/><path d="M402 40l6-8 6 8-6-2Z" class="snow"/></g>
      ${[[40, 372], [58, 440], [150, 446], [258, 440], [52, 176], [232, 246], [44, 112], [230, 42], [612, 300], [520, 176]].map(([x, y]) => tree(x, y)).join('')}
      <g class="city">${[[588, 418, 14, 44], [604, 400, 12, 62], [618, 426, 12, 36], [312, 420, 10, 34], [324, 408, 12, 46]].map(([x, y, w, h]) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="1.5"/><rect class="lit" x="${x + 3}" y="${y + 6}" width="2.5" height="2.5"/><rect class="lit" x="${x + w - 5.5}" y="${y + 14}" width="2.5" height="2.5"/>`).join('')}</g>
      <path id="road" class="road-casing" d="${road}"/><path class="road" d="${road}"/><path class="road-line" d="${road}"/>
      ${still ? '' : `<circle class="traveller" r="4.5"><animateMotion dur="16s" repeatCount="indefinite" rotate="auto"><mpath href="#road"/></animateMotion></circle>`}
      ${houses}
      <g class="here" transform="translate(${hx} ${hy - 40})" pointer-events="none"><circle class="pulse" r="9"/><path class="pin" d="M0 6c-5-6-8-9.5-8-13a8 8 0 0 1 16 0c0 3.5-3 7-8 13z"/><circle cx="0" cy="-7" r="3" fill="#0b0d12"/>
        <g transform="translate(14 -16)"><rect x="0" y="-11" width="${textWidth(t('youAreHere'), 11) + 14}" height="20" rx="10"/><text x="7" y="3">${t('youAreHere')}</text></g></g>
      <g class="compass" transform="translate(604 38)"><circle r="17"/><path d="M0 -12l4 12h-8Z" class="n"/><path d="M0 12l4-12h-8Z"/><text y="-20">N</text></g>
    </svg>`;
  }

  /* ------------------------------------------------------------ detail */
  function detailView(id) {
    const c = BY_ID[id];
    if (!c) return notFoundView();
    store.set('leon-learn-recent', [id, ...recent().filter((x) => x !== id)].slice(0, 6));
    const pr = courseProgress(c);
    const at = pr ? chapterIndex(c, pr.topic) : -1;
    const rl = readLang(c);
    const chapterNo = Object.fromEntries(c.chapters.map((ch, i) => [ch.id, i + 1]));
    const byId = Object.fromEntries(c.chapters.map((ch) => [ch.id, ch]));
    const stages = c.stages.map((s, si) => `<div class="stage"><div class="stage-head"><h3>${pad(si + 1)} · ${esc(L(s.title))}</h3><span>${t('chaptersCount')(s.chapters.length)}</span></div>` +
      s.chapters.map((cid) => {
        const ch = byId[cid];
        const langs = c.langs.map((l) => `<a href="${readUrl(c, cid, l)}" lang="${l}">${l === 'zh' ? '中文' : 'EN'}</a>`).join('');
        return `<div class="chapter${pr && pr.topic === cid ? ' current' : ''}"><span class="no">${pad(chapterNo[cid])}</span><span><a class="ttl" href="${readUrl(c, cid, rl)}">${esc(L(ch.title))}</a><span class="alt">${esc(other(ch.title) || '')}</span></span><span class="langs">${langs}</span></div>`;
      }).join('') + '</div>').join('');
    const facts = [['chapters', c.stats.chapters], ['programs', c.stats.programs], ['problems', c.stats.problems], ['exercises', c.stats.exercises], ['projects', c.stats.projects]]
      .filter(([, v]) => v).slice(0, 3)
      .map(([k, v]) => `<div><dt>${t('facts')[k]}</dt><dd class="num">${v}</dd></div>`).join('') +
      `<div><dt>${t('facts').language}</dt><dd class="text">${c.langs.length > 1 ? t('bilingual') : t('zhOnly')}</dd></div>`;
    const otherL = rl === 'zh' ? 'en' : 'zh';
    const sheet = c.sheet ? `<section class="panel"><div class="panel-head"><h2>${t('sheetTitle')}</h2></div><div class="panel-body">
        <a class="btn ghost" href="${SITE + c.sheet[c.sheet[lang] ? lang : 'zh']}">${icon('sheet')}${c.pdf ? t('sheetWeb') : t('sheetSection')}</a>
        ${c.pdf ? `<a class="btn ghost" href="${SITE + c.pdf}" download>${icon('down')}${t('sheetPdf')}</a>` : ''}
        <a class="btn ghost" href="${SITE + c.notes[c.notes[lang] ? lang : 'zh']}" download>${icon('down')}${c.notesKind === 'zip' ? t('notesZip') : t('notesMd')}</a></div></section>` : '';
    return frame('detail', `<nav class="crumbs"><a href="${href.list}">${t('list')}</a><span>/</span><span>${esc(c.code)}</span></nav>
      <section class="panel reveal" style="--accent:${c.color}">
        <div class="detail-head">${tile(c, true)}<div><div class="tags"><span class="code">${esc(c.code)}</span>${levelTag(c)}${langTag(c)}<span class="tag">${esc(L(DATA.tracks[c.track]))}</span></div>
          <h1>${esc(L(c.title))}</h1><p class="alt">${esc(other(c.title) || '')}</p><p class="desc">${esc(L(c.description))}</p></div>
          <div class="head-actions"><button type="button" class="star" data-star="${c.id}" aria-pressed="${stars().includes(c.id)}" aria-label="${stars().includes(c.id) ? t('unstar') : t('star')}">${icon('star')}</button></div></div>
        <dl class="facts">${facts}</dl>${stageBar(c)}
      </section>
      <div class="detail-grid" style="--accent:${c.color}">
        <section class="panel reveal d1"><div class="panel-head"><h2>${t('toc')}</h2><span class="muted">${t('chaptersCount')(c.chapters.length)}</span></div>${stages}</section>
        <div class="side reveal d2">
          <section class="panel"><div class="panel-body">
            ${at >= 0 ? `<div class="resume-mini"><small>${t('continueAt')}</small>${pad(at + 1)} · ${esc(pr.title)}</div><a class="btn primary" href="${SITE + esc(pr.url)}">${t('resumeBtn')} ${icon('arrow')}</a>` : ''}
            <a class="btn ${at >= 0 ? 'ghost' : 'primary'}" href="${readUrl(c, c.chapters[0].id, rl)}">${t('startRead')} ${icon('arrow')}</a>
            ${c.read[otherL] ? `<a class="btn ghost" href="${readUrl(c, '', otherL)}" lang="${otherL}">${icon('globe')}${t('otherLang')}</a>` : `<p class="muted" style="font-size:12.5px;text-align:center">${t('otherLangOnly')}</p>`}
          </div></section>
          ${sheet}
          <section class="panel"><div class="panel-head"><h2>${t('before')}</h2></div><div class="panel-body"><ul>${L(c.prerequisites).map((x) => `<li>${esc(x)}</li>`).join('')}</ul></div></section>
          <section class="panel"><div class="panel-head"><h2>${t('outcomes')}</h2></div><div class="panel-body"><ul>${L(c.outcomes).map((x) => `<li>${esc(x)}</li>`).join('')}</ul></div></section>
        </div>
      </div>`);
  }

  /* ------------------------------------------------------------ route, sheets, mine */
  function routeView() {
    const stages = DATA.route.map((r, i) => `<section class="route-stage reveal${i ? ` d${Math.min(i, 3)}` : ''}" data-track="${r.track}"><div class="route-rail"><b>${i + 1}</b></div><div class="route-body">
      <h2>${esc(L(DATA.tracks[r.track]))}</h2><p>${esc(L(r.note))}</p><div class="route-cards">` +
      r.courses.map((id) => { const c = BY_ID[id]; return `<a class="panel route-card" href="${href.course(id)}" style="--accent:${c.color}">${tile(c)}<span><span class="code">${esc(c.code)}</span><b>${esc(L(c.title))}</b><small>${c.stats.chapters} ${t('chaptersUnit')} · ${c.langs.length > 1 ? t('bilingual') : t('zhOnly')}</small></span></a>`; }).join('') +
      '</div></div></section>').join('');
    return frame('route', `<div class="page-head"><div><h1>${t('route')}</h1><p>${t('routeSub')}</p></div></div><div class="route">${stages}</div>`);
  }

  function sheetsView() {
    const cards = DATA.courses.filter((c) => c.sheet).map((c) => {
      const l = c.sheet[lang] ? lang : 'zh';
      const note = c.pdf ? `${t('sheetWeb')} · ${t('sheetPdf')}` : (c.id === 'python' ? t('pythonSheet') : t('reviewNote'));
      return `<article class="panel sheet" style="--accent:${c.color}"><div class="top">${tile(c)}<div><span class="code">${esc(c.code)}</span><b>${esc(L(c.title))}</b><small>${note}</small></div></div>
        <div class="links"><a class="btn ghost sm" href="${SITE + c.sheet[l]}">${icon('sheet')}${c.pdf ? t('sheetWeb') : t('sheetSection')}</a>${c.pdf ? `<a class="btn ghost sm" href="${SITE + c.pdf}" download>${icon('down')}PDF</a>` : ''}</div></article>`;
    }).join('');
    return frame('sheets', `<div class="page-head"><div><h1>${t('sheets')}</h1><p>${t('sheetsSub')}</p></div></div>
      <div class="sheet-grid reveal"><article class="panel sheet feature"><div class="top"><span class="icon-tile lg">${icon('sheet')}</span><div><b>${t('collection')}</b><small>${t('collectionNote')}</small></div></div><a class="btn primary" href="${SITE + DATA.collection}" download>${icon('down')}${t('download')}</a></article>${cards}</div>`);
  }

  function mineView() {
    const p = progress();
    const lastItems = Object.entries(p.courses || {}).filter(([id]) => BY_ID[id]).sort((a, b) => (b[1].time || 0) - (a[1].time || 0));
    const item = (c, sub, to) => `<li><a href="${to}" style="--accent:${c.color}">${tile(c)}<span><b>${esc(c.code)} · ${esc(L(c.title))}</b><small>${esc(sub)}</small></span></a></li>`;
    const last = lastItems.length ? `<ul class="mini-list">${lastItems.map(([id, v]) => item(BY_ID[id], `${pad(chapterIndex(BY_ID[id], v.topic) + 1)} · ${v.title}`, SITE + esc(v.url))).join('')}</ul>` : `<div class="empty">${t('emptyLast')}</div>`;
    const st = stars().filter((id) => BY_ID[id]);
    const starred = st.length ? `<ul class="mini-list">${st.map((id) => item(BY_ID[id], other(BY_ID[id].title) || L(BY_ID[id].subtitle), href.course(id))).join('')}</ul>` : `<div class="empty">${t('emptyStars')}</div>`;
    const rc = recent();
    const rec = rc.length ? `<ul class="mini-list">${rc.map((id) => item(BY_ID[id], L(BY_ID[id].subtitle), href.course(id))).join('')}</ul>` : `<div class="empty">${t('emptyRecent')}</div>`;
    return frame('mine', `<div class="page-head"><div><h1>${t('mine')}</h1><p>${t('mineSub')}</p></div><button type="button" class="btn ghost sm" data-clear>${t('clear')}</button></div>
      <div class="mine-grid reveal"><section class="panel"><div class="panel-head"><h2>${t('last')}</h2></div>${last}</section>
      <section class="panel"><div class="panel-head"><h2>${t('starred')}</h2></div>${starred}</section>
      <section class="panel"><div class="panel-head"><h2>${t('recentT')}</h2></div>${rec}</section></div>`);
  }

  function notFoundView() {
    return frame('', `<div class="panel empty" style="padding:60px 20px"><p>${t('notFound')}</p><p style="margin-top:14px"><a class="btn ghost" href="${href.list}">${t('back')}</a></p></div>`);
  }

  /* ------------------------------------------------------------ router */
  const parse = () => {
    const parts = location.hash.replace(/^#\/?/, '').split('/').filter(Boolean);
    if (!parts.length) return { page: 'intro' };
    if (parts[0] === 'courses') return { page: 'list' };
    if (parts[0] === 'course') return { page: 'detail', id: parts[1] };
    if (['route', 'sheets', 'mine'].includes(parts[0])) return { page: parts[0] };
    return { page: 'missing' };
  };
  const TITLES = { intro: () => `${t('brand')} · ${t('heroA')}`, list: () => t('list'), route: () => t('route'), sheets: () => t('sheets'), mine: () => t('mine') };
  let lastPage = '';
  function render() {
    timers.forEach(clearInterval); timers = [];
    if (observer) { observer(); observer = null; }
    const r = parse();
    document.documentElement.lang = lang === 'zh' ? 'zh-Hans' : 'en';
    const views = { intro: introView, list: listView, detail: () => detailView(r.id), route: routeView, sheets: sheetsView, mine: mineView, missing: notFoundView };
    app.innerHTML = views[r.page]();
    const name = r.page === 'detail' && BY_ID[r.id] ? `${BY_ID[r.id].code} · ${L(BY_ID[r.id].title)}` : (TITLES[r.page] || (() => t('brand')))();
    document.title = r.page === 'intro' ? name : `${name} · ${t('brand')}`;
    if (r.page === 'intro') wireIntro();
    if (r.page === 'list') wireList();
    const key = r.page + (r.id || '');
    if (key !== lastPage) window.scrollTo(0, 0);
    lastPage = key;
  }

  app.addEventListener('click', (e) => {
    const langBtn = e.target.closest('[data-lang]');
    if (langBtn) { setLang(langBtn.dataset.lang); const y = window.scrollY; render(); window.scrollTo(0, y); return; }
    const starBtn = e.target.closest('[data-star]');
    if (starBtn) {
      const id = starBtn.dataset.star;
      const s = stars();
      const next = s.includes(id) ? s.filter((x) => x !== id) : [...s, id];
      store.set('leon-learn-stars', next);
      starBtn.setAttribute('aria-pressed', String(next.includes(id)));
      starBtn.setAttribute('aria-label', next.includes(id) ? t('unstar') : t('star'));
      return;
    }
    if (e.target.closest('[data-clear]')) {
      ['leon-learn-stars', 'leon-learn-recent', 'leon-learn-progress'].forEach(store.remove);
      render();
    }
  });
  window.addEventListener('hashchange', render);
  if (parse().page === 'intro' && store.get('leon-learn-skip-intro', false) && !location.hash) location.replace(href.list);
  render();
})();
