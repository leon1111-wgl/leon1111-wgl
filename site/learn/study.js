/* Learning hub: goals and routes, practice, mock papers and the review queue. Loaded before learn.js, which calls init.
   All progress stays in this browser (leon-learn-* keys); "My learning" can back it up to a file. */
window.LeonStudyInit = (hub) => {
  const { store, esc, icon, frame, BY_ID, DATA, SITE, href } = hub;
  const lang = () => hub.lang();
  const L = (o) => (o && typeof o === 'object' && !Array.isArray(o) ? (o[lang()] ?? o.zh ?? o.en) : o);
  // reader text may use `code` and **bold**
  const inline = (s) => esc(s).replace(/`([^`\n]+)`/g, '<code>$1</code>').replace(/\*\*(\S(?:[^*\n]*\S)?)\*\*/g, '<b>$1</b>');
  const rich = (s) => String(s ?? '').split('\n\n').map((p) => `<p>${inline(p).replace(/\n/g, '<br>')}</p>`).join('');
  const para = rich;
  const now = () => Date.now();
  const F = () => globalThis.LeonFSRS;
  const COURSE_IDS = ['python', 'info1113', 'comp2017', 'comp2123', 'comp2022', 'comp3308', 'start', 'ml', 'dl', 'vision', 'multimodal'];
  const PAPER_LANGS = [['comp2017', 'C'], ['info1113', 'Java'], ['python', 'Python'], ['comp2123', 'Python']];

  /* ------------------------------------------------------------ text */
  const TEXT = {
    zh: {
      navPractice: '练习', navReview: '复习', navStart: '我的路线', sStart: '路线', sPractice: '练习', sReview: '复习',
      startTitle: '你想达到什么目标？', startSub: '选一个，给你一条具体路线。随时可以换。进度只保存在这个浏览器里。',
      goals: {
        zero: ['我从没写过代码', '不需要任何基础。每一步都先讲清楚，再动手，每个术语都解释。'],
        exam: ['我要考试', '先做小测找出薄弱点，再按时间安排复习、刷题和模拟卷。'],
        paper: ['我要手写代码', '不靠自动补全和运行：先预测输出、填跟踪表、画内存图，再在纸上写并对照评分标准。'],
        engineer: ['我在工作中写代码', '工具、调试、测试、代码审查和生产环境的取舍，配真实可复现的实验。'],
      },
      chooseCourse: '选一门课', choosePaper: '选一门语言', pace: '离考试还有多久？', paces: { week: '一周左右', month: '一个月左右', later: '更久' },
      nextStep: '下一步', routeDone: '这条路线走完了。挑一门新课，或者继续每天复习。', markDone: '完成了', markUndo: '撤销完成', stepsDone: (a, n) => `已完成 ${a} / ${n} 步`, changeGoal: '换一个目标', yourRoute: '你的路线', minutes: (m) => `约 ${m} 分钟`, openStep: '开始',
      unofficial: '这是独立整理的非官方练习。题目全部原创，不是往年考题，也不代表任何真实考试的内容或形式。',
      practiceTitle: '练习', practiceSub: '先自己做，再看答案。代码题都已实际运行核对过。', reviewDue: (n) => `${n} 张到期`,
      kinds: { predict: '预测输出', worked: '推导题', mcq: '选择题', numeric: '计算题', trace: '跟踪表', write: '手写代码', memory: '内存图', short: '简答题', bug: '找错题', proof: '证明题', design: '算法设计' },
      kindsAll: '全部题型', topicsAll: '全部章节', noQuestions: '这个筛选下没有题目。', qCount: (n) => `${n} 题`, cardsCount: (n) => `${n} 张复习卡`, papersCount: (n) => `${n} 套模拟卷`, marks: (n) => `${n} 分`,
      scored: (a, b) => `${a} / ${b} 分`, notTried: '未做', startSet: '来 10 题', continueSet: '继续下一题', weakTitle: '该复习哪些章节', weakSub: '按你做过的题算得分率，最低的排在前面。', weakEmpty: '做几题之后，这里会告诉你该复习什么。', chapterRead: '读这一章', weakPractice: '练这一章',
      backList: '返回题目列表', next: '下一题', prev: '上一题', check: '核对答案', reveal: '看答案和评分标准', yourAnswer: '你的答案', predictPrompt: '不要运行。写出这段程序会打印的全部内容。', predictHint: '逐行写。行尾空格不影响得分。', expected: '正确输出', yours: '你写的', lineOk: '对', lineBad: '不对', walk: '逐步解释', traceT: '执行过程', runIt: '运行核对', running: '运行中…', ranOut: '实际输出',
      workedPrompt: '先在纸上或下面的框里自己算。想好了再看方法。', showMethod: '看方法', strategy: '怎样选方法', nextStepBtn: '看下一步', hadStep: '这一步我也做对了', answer: '答案', sanity: '再检查一遍', finishMark: '记下得分',
      paperMode: '手写模式', paperNote: '关掉编辑器，拿纸和笔。不查资料，不运行，写完再看答案。', paperTimer: '建议用时', startTimer: '开始计时', timerRun: '用时', typeHere: '也可以写在这里（没有补全和高亮）', model: '参考答案', rubric: '评分标准（做到的打勾）', mistakes: '手写时常见的错误', yourScore: '你的得分', runTests: '现在敲进去运行', testsPass: '测试全部通过', testsFail: '测试没有全部通过', typed: '你的代码', given: '已知代码', solution: '解答',
      correct: '正确', wrong: '不对', chooseOne: '选一个答案', numberPlaceholder: '填写数字', toleranceNote: (t) => `允许误差 ±${t}`, traceFill: '不要运行。把空格填完。', cellsRight: (a, n) => `${a} / ${n} 格正确`,
      addReview: '加入复习', addedReview: '已加入复习', autoAdded: '没拿满分的题已加入复习队列。',
      examsTitle: '模拟卷', examIntro: '限时做完再看答案。选择、计算和跟踪题自动判分；写代码和简答题按评分标准自己打分。', examStart: '开始计时', examResume: '继续作答', examRedo: '重新做一次', examSubmit: '交卷', examConfirm: '确定交卷吗？', timeLeft: '剩余', timeUp: '时间到。可以交卷了。', examResult: '成绩', examSelf: '这一题需要你按评分标准自己打分。', examAuto: '自动判分', examByTopic: '各章得分率', examAddMissed: '把丢分的题加入复习', examDone: '已加入', examTotal: (a, b) => `${a} / ${b} 分`, examPaperNote: '建议在纸上作答，再把答案填到框里。', examMins: (m) => `${m} 分钟`, examAgain: '再做一次', examLast: (a, b) => `上次 ${a} / ${b}`,
      reviewTitle: '复习队列', reviewSub: '每天做一点。系统用 FSRS-6 算法（默认参数）安排下一次复习的时间，快要忘的时候再问你。', dueNow: '现在到期', newCards: '新卡片', allCards: '全部卡片', startReview: '开始复习', nothingDue: '现在没有到期的卡片。', addDeck: '加入复习', addRead: '加入已读章节', addAll: '加入全部', inDeck: (a, b) => `已加入 ${a} / ${b} 张`, missedInDeck: (n) => `另有 ${n} 道错题`, showAnswer: '看答案', again: '忘了', hard: '有点难', good: '记得', easy: '很轻松', days: (d) => (d <= 0 ? '今天' : d === 1 ? '1 天后' : d < 30 ? `${d} 天后` : d < 365 ? `${Math.round(d / 30)} 个月后` : `${(d / 365).toFixed(1)} 年后`), sessionDone: '这一轮复习完了', sessionStats: (n) => `复习了 ${n} 张。明天再来。`, cardOf: (a, n) => `第 ${a} / ${n} 张`, newLimit: (n) => `每天最多 ${n} 张新卡片`, reviewEmpty: '还没有卡片。从下面加入一门课，或者读完一章后再加。',
      backupTitle: '备份进度', backupSub: '进度只在这个浏览器里。换设备前可以导出成文件，再导入。', exportB: '导出', importB: '导入', importedOk: '已导入，页面将刷新。', importBad: '这个文件无法读取。', stageName: '章节',
      chineseChapters: '题目有中英文；章节是中文', loading: '加载中…', loadFail: '题库没有加载成功。检查网络后再试。', tryAgain: '再试一次',
      resumeRoute: '接着走你的路线', reviewToday: '今天的复习', cardsReady: (n) => `${n} 张卡片可以复习`,
      glance: '一眼看清进度', glanceRoute: '路线', glanceReview: '复习', glanceDue: (n, all) => `今天到期 ${n} 张 · 队列里共 ${all} 张`, glancePractice: '练习',
      glanceScore: (q, pct) => `做过 ${q} 题 · 得分率 ${pct}%`, glanceRead: '阅读', glanceReadN: (a, n) => `读完 ${a} / ${n} 章`, glanceEmpty: '还没有记录。做完一道题、读完一章或者选一条路线后，这里会显示进度。', glanceOpen: '打开',
      chooseGoal: '先选一个目标', chooseGoalSub: '告诉我们你想做什么，给你一条具体路线。',
      labsTitle: '工程实验', labsSub: '每个实验都在持续集成里实际跑过，页面上是当时的输出。', labSteps: '步骤', labScenario: '场景', labReview: '代码审查清单', labTrade: '生产环境的取舍', labCheck: '做到这些才算完成', labCaptured: '实际输出',
    },
    en: {
      navPractice: 'Practice', navReview: 'Review', navStart: 'My route', sStart: 'Route', sPractice: 'Practice', sReview: 'Review',
      startTitle: 'What do you want to do?', startSub: 'Pick one and get a concrete route. You can change it any time. Progress stays in this browser.',
      goals: {
        zero: ['I have never programmed', 'No background needed. Each step is explained before you try it, and every term is defined.'],
        exam: ['I have an exam coming', 'Find your weak spots with a short test, then revise, practise and sit timed mock papers.'],
        paper: ['I must write code by hand', 'No autocomplete, no running: predict output, fill trace tables, draw memory, then write on paper and mark it against a rubric.'],
        engineer: ['I write code at work', 'Tools, debugging, testing, code review and production trade-offs, with realistic labs you can reproduce.'],
      },
      chooseCourse: 'Choose a course', choosePaper: 'Choose a language', pace: 'How long until the exam?', paces: { week: 'About a week', month: 'About a month', later: 'Longer' },
      nextStep: 'Next step', routeDone: 'You finished this route. Pick a new course, or keep up the daily review.', markDone: 'Mark done', markUndo: 'Undo', stepsDone: (a, n) => `${a} of ${n} steps done`, changeGoal: 'Change goal', yourRoute: 'Your route', minutes: (m) => `about ${m} min`, openStep: 'Open',
      unofficial: 'Independent, unofficial practice. All questions are original. They are not past papers and do not indicate what a real exam will contain or look like.',
      practiceTitle: 'Practice', practiceSub: 'Try first, then check. Every code question has been run to confirm the answer.', reviewDue: (n) => `${n} due`,
      kinds: { predict: 'Predict the output', worked: 'Worked problem', mcq: 'Multiple choice', numeric: 'Calculation', trace: 'Trace table', write: 'Write code', memory: 'Memory diagram', short: 'Short answer', bug: 'Find the bug', proof: 'Proof', design: 'Algorithm design' },
      kindsAll: 'All types', topicsAll: 'All chapters', noQuestions: 'No questions match this filter.', qCount: (n) => `${n} question${n === 1 ? '' : 's'}`, cardsCount: (n) => `${n} review cards`, papersCount: (n) => `${n} mock paper${n === 1 ? '' : 's'}`, marks: (n) => `${n} mark${n === 1 ? '' : 's'}`,
      scored: (a, b) => `${a} / ${b} marks`, notTried: 'Not tried', startSet: 'Do 10 questions', continueSet: 'Next question', weakTitle: 'What to revise', weakSub: 'Your score rate by chapter from the questions you tried, lowest first.', weakEmpty: 'Try a few questions and this will tell you what to revise.', chapterRead: 'Read chapter', weakPractice: 'Practise it',
      backList: 'Back to the list', next: 'Next question', prev: 'Previous', check: 'Check my answer', reveal: 'Show answer and rubric', yourAnswer: 'Your answer', predictPrompt: 'Do not run it. Write everything this program prints.', predictHint: 'One line at a time. Trailing spaces are ignored.', expected: 'Correct output', yours: 'You wrote', lineOk: 'Right', lineBad: 'Wrong', walk: 'Step by step', traceT: 'Execution trace', runIt: 'Run to confirm', running: 'Running…', ranOut: 'Actual output',
      workedPrompt: 'Work it out on paper or in the box first. Open the method when you have an answer.', showMethod: 'Show the method', strategy: 'Choosing a method', nextStepBtn: 'Next step', hadStep: 'I got this step', answer: 'Answer', sanity: 'Check it again', finishMark: 'Record my score',
      paperMode: 'Paper mode', paperNote: 'Close your editor and take a pen and paper. No notes, no running. Look at the answer only when you finish.', paperTimer: 'Suggested time', startTimer: 'Start timer', timerRun: 'Time', typeHere: 'Or write here (no autocomplete or highlighting)', model: 'Model answer', rubric: 'Rubric (tick what you did)', mistakes: 'Common handwriting mistakes', yourScore: 'Your score', runTests: 'Now type it in and run it', testsPass: 'All tests pass', testsFail: 'Not all tests pass', typed: 'Your code', given: 'Given code', solution: 'Solution',
      correct: 'Correct', wrong: 'Not quite', chooseOne: 'Choose an answer', numberPlaceholder: 'Enter a number', toleranceNote: (t) => `within ±${t}`, traceFill: 'Do not run it. Fill in the blanks.', cellsRight: (a, n) => `${a} of ${n} cells right`,
      addReview: 'Add to review', addedReview: 'In your review queue', autoAdded: 'Questions without full marks were added to your review queue.',
      examsTitle: 'Mock papers', examIntro: 'Finish within the time, then see the answers. Multiple choice, calculations and traces mark themselves; you mark written answers against the rubric.', examStart: 'Start the clock', examResume: 'Continue', examRedo: 'Start again', examSubmit: 'Hand in', examConfirm: 'Hand in now?', timeLeft: 'Left', timeUp: 'Time is up. Hand in when ready.', examResult: 'Result', examSelf: 'Mark this one yourself against the rubric.', examAuto: 'Marked automatically', examByTopic: 'Score rate by chapter', examAddMissed: 'Add lost marks to review', examDone: 'Added', examTotal: (a, b) => `${a} / ${b} marks`, examPaperNote: 'Best done on paper; then type your answers into the boxes.', examMins: (m) => `${m} minutes`, examAgain: 'Sit it again', examLast: (a, b) => `Last time ${a} / ${b}`,
      reviewTitle: 'Review queue', reviewSub: 'A little each day. The FSRS-6 algorithm with its default parameters schedules each card for when you are about to forget it.', dueNow: 'Due now', newCards: 'New', allCards: 'All cards', startReview: 'Start reviewing', nothingDue: 'Nothing is due right now.', addDeck: 'Add to review', addRead: 'Add chapters I read', addAll: 'Add all', inDeck: (a, b) => `${a} of ${b} cards added`, missedInDeck: (n) => `plus ${n} missed question${n === 1 ? '' : 's'}`, showAnswer: 'Show answer', again: 'Forgot', hard: 'Hard', good: 'Good', easy: 'Easy', days: (d) => (d <= 0 ? 'today' : d === 1 ? 'in 1 day' : d < 30 ? `in ${d} days` : d < 365 ? `in ${Math.round(d / 30)} mo` : `in ${(d / 365).toFixed(1)} yr`), sessionDone: 'Round finished', sessionStats: (n) => `You reviewed ${n} card${n === 1 ? '' : 's'}. Come back tomorrow.`, cardOf: (a, n) => `Card ${a} of ${n}`, newLimit: (n) => `At most ${n} new cards a day`, reviewEmpty: 'No cards yet. Add a course below, or add chapters as you finish them.',
      backupTitle: 'Back up your progress', backupSub: 'Progress lives in this browser only. Export it to a file before you change device, then import it.', exportB: 'Export', importB: 'Import', importedOk: 'Imported. The page will reload.', importBad: 'That file could not be read.', stageName: 'Chapter',
      chineseChapters: 'Questions in both languages; its chapters are in Chinese', loading: 'Loading…', loadFail: 'The question bank did not load. Check your connection and try again.', tryAgain: 'Try again',
      resumeRoute: 'Continue your route', reviewToday: "Today's review", cardsReady: (n) => `${n} card${n === 1 ? '' : 's'} ready to review`,
      glance: 'Progress at a glance', glanceRoute: 'Route', glanceReview: 'Review', glanceDue: (n, all) => `${n} due today · ${all} in the queue`, glancePractice: 'Practice',
      glanceScore: (q, pct) => `${q} question${q === 1 ? '' : 's'} tried · ${pct}% of marks`, glanceRead: 'Reading', glanceReadN: (a, n) => `${a} of ${n} chapters read`, glanceEmpty: 'Nothing yet. Answer a question, finish a chapter or choose a route, and your progress shows here.', glanceOpen: 'Open',
      chooseGoal: 'Choose a goal first', chooseGoalSub: 'Tell us what you want to do and get a concrete route.',
      labsTitle: 'Engineering labs', labsSub: 'Every lab is run in continuous integration, and the page shows the output of that run.', labSteps: 'Steps', labScenario: 'Scenario', labReview: 'Code review checklist', labTrade: 'Production trade-offs', labCheck: 'Done when', labCaptured: 'Actual output',
    },
  };
  const t = (key) => TEXT[lang()][key];

  /* ------------------------------------------------------------ data and storage */
  const cache = new Map();
  const loadCourse = (cid) => {
    if (!cache.has(cid)) {
      cache.set(cid, fetch(`data/${cid}.json`).then((r) => { if (!r.ok) throw new Error(String(r.status)); return r.json(); }).then((d) => { cache.set(`${cid}:ready`, d); return d; }));
    }
    return cache.get(cid);
  };
  const ready = (cid) => cache.get(`${cid}:ready`);
  /* a view that needs a course file shows a loading line, then renders again once it arrives */
  const withCourse = (cid, active, view) => {
    const data = ready(cid);
    if (data) return view(data);
    loadCourse(cid).then(() => hub.render(), () => {
      cache.delete(cid); // so that trying again really fetches again
      const box = hub.app.querySelector('[data-load]');
      if (!box) return;
      box.textContent = `${t('loadFail')} `;
      const retry = Object.assign(document.createElement('button'), { type: 'button', className: 'btn ghost sm', textContent: t('tryAgain') });
      retry.addEventListener('click', () => hub.render());
      box.append(retry);
    });
    return frame(active, `<div class="panel empty" data-load>${t('loading')}</div>`);
  };
  const attempts = () => store.get('leon-learn-attempts', {});
  const setAttempt = (key, score, marks, { sameTry = false } = {}) => {
    const all = attempts();
    const prev = all[key];
    all[key] = { score, marks, best: Math.max(score, prev?.best ?? 0), n: (prev?.n ?? 0) + (sameTry ? 0 : 1), at: now() };
    store.set('leon-learn-attempts', all);
  };
  const srs = () => store.get('leon-learn-srs', {});
  const setSrs = (value) => store.set('leon-learn-srs', value);
  const inQueue = (key) => key in srs();
  const enqueue = (keys) => { const s = srs(); keys.forEach((k) => { if (!(k in s)) s[k] = { fresh: true, added: now() }; }); setSrs(s); };
  const goalState = () => store.get('leon-learn-goal', null);
  const setGoal = (value) => store.set('leon-learn-goal', value);
  const routeKey = (goal, course) => `${goal}/${course || ''}`;
  const routeDone = (goal, course) => store.get('leon-learn-routes', {})[routeKey(goal, course)] || {};
  const setRouteDone = (goal, course, done) => store.set('leon-learn-routes', { ...store.get('leon-learn-routes', {}), [routeKey(goal, course)]: done });
  const paperKey = (cid, pid) => `leon-learn-paper:${cid}/${pid}`;
  const NEW_PER_DAY = 20;
  const dayStamp = () => { const d = new Date(); return `${d.getFullYear()}-${d.getMonth() + 1}-${d.getDate()}`; };
  const courseName = (cid) => (BY_ID[cid] ? `${BY_ID[cid].code} · ${L(BY_ID[cid].title)}` : cid);
  const chapterTitle = (cid, tid) => { const ch = BY_ID[cid]?.chapters.find((x) => x.id === tid); return ch ? L(ch.title) : tid; };
  const chapterUrl = (cid, tid) => { const c = BY_ID[cid]; const l = c.read[lang()] ? lang() : c.langs[0]; return `${SITE}${c.read[l]}#${tid}`; };
  const readCount = (cid) => new Set(store.get('leon-learn-progress', { courses: {} }).courses?.[cid]?.read || []);

  /* ------------------------------------------------------------ marking */
  const normLine = (s) => s.replace(/\s+$/, '');
  const normCell = (s) => String(s ?? '').trim().replace(/\s+/g, ' ').toLowerCase();
  const markPredict = (q, answer) => {
    const want = q.output.replace(/\n$/, '').split('\n').map(normLine);
    const got = answer.replace(/\r/g, '').replace(/\n+$/, '').split('\n').map(normLine);
    const lines = want.map((w, i) => ({ want: w, got: got[i] ?? '', ok: got[i] === w }));
    const extra = got.slice(want.length).filter(Boolean);
    const right = lines.filter((x) => x.ok).length;
    // any wrong line costs at least a share of the marks: full marks only for a fully right answer
    const score = Math.max(0, Math.floor(((right - extra.length) / want.length) * q.marks));
    return { score, lines, extra };
  };
  const markMcq = (q, chosen) => (q.options[chosen]?.correct ? q.marks : 0);
  const markNumeric = (q, value) => {
    const got = Number(String(value).replace(/,/g, '').trim());
    if (value === '' || value == null || !Number.isFinite(got)) return 0;
    return Math.abs(got - q.answer) <= (q.tolerance ?? 0) + 1e-12 ? q.marks : 0;
  };
  /* trace rows: a null-free table in the data; `given` lists "r,c" cells shown filled in */
  const markTrace = (q, cells) => {
    const blanks = traceBlanks(q);
    const right = blanks.filter(([r, c]) => normCell(cells[`${r},${c}`]) === normCell(q.rows[r][c])).length;
    return { right, total: blanks.length, score: blanks.length ? Math.round((right / blanks.length) * q.marks) : 0 };
  };
  const traceBlanks = (q) => {
    const given = new Set(q.given || []);
    const out = [];
    q.rows.forEach((row, r) => row.forEach((_, c) => { if (!given.has(`${r},${c}`) && c !== 0) out.push([r, c]); }));
    return out;
  };
  // Options show in a shuffled order fixed per question: position gives nothing away, and a refresh keeps the order.
  const optionOrder = (q) => {
    let seed = 0;
    for (const ch of q.id) seed = (Math.imul(seed, 31) + ch.charCodeAt(0)) >>> 0;
    const order = q.options.map((_, i) => i);
    for (let i = order.length - 1; i > 0; i -= 1) {
      seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0;
      const j = seed % (i + 1);
      [order[i], order[j]] = [order[j], order[i]];
    }
    return order;
  };
  const AUTO = new Set(['predict', 'mcq', 'numeric', 'trace']);
  const canRun = (language) => { try { return typeof Worker !== 'undefined' && (language !== 'java' || WebAssembly.validate(new Uint8Array([0, 97, 115, 109, 1, 0, 0, 0, 1, 5, 1, 95, 1, 127, 0]))); } catch (_) { return false; } };

  /* ------------------------------------------------------------ pieces */
  const crumbs = (...parts) => `<nav class="crumbs">${parts.map((p, i) => (i === parts.length - 1 ? `<span>${esc(p[0])}</span>` : `<a href="${p[1]}">${esc(p[0])}</a><span>/</span>`)).join('')}</nav>`;
  const unofficial = () => `<p class="study-note">${t('unofficial')}</p>`;
  const codeBlock = (code) => `<pre class="study-code" tabindex="0">${esc(code)}</pre>`;
  const traceTable = (trace) => `<div class="study-trace" tabindex="0"><table><thead><tr>${L(trace.columns).map((c) => `<th>${esc(c)}</th>`).join('')}</tr></thead><tbody>${L(trace.rows).map((r) => `<tr>${r.map((c) => `<td>${esc(c)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
  const badge = (q) => `<span class="tag accent">${esc(t('kinds')[q.kind] || q.kind)}</span><span class="tag">${esc(t('marks')(q.marks))}</span>${q.language ? `<span class="tag">${esc({ c: 'C', java: 'Java', python: 'Python' }[q.language])}</span>` : ''}${q.minutes ? `<span class="tag">${esc(t('minutes')(q.minutes))}</span>` : ''}`;
  const attemptTag = (a) => (a ? `<span class="q-score ${a.best >= a.marks ? 'full' : a.best > 0 ? 'part' : 'zero'}">${a.best} / ${a.marks}</span>` : `<span class="q-score none">${t('notTried')}</span>`);

  /* ------------------------------------------------------------ goal and route */
  function startView() {
    const g = goalState();
    const cards = Object.entries(t('goals')).map(([id, [title, sub]]) => `<a class="panel goal-card${g?.goal === id ? ' current' : ''}" href="#/goal/${id}"><span class="icon-tile lg">${icon({ zero: 'story', exam: 'quiz', paper: 'sheet', engineer: 'code' }[id])}</span><span><b>${esc(title)}</b><small>${esc(sub)}</small></span></a>`).join('');
    return frame('start', `<div class="page-head"><div><h1>${t('startTitle')}</h1><p>${t('startSub')}</p></div></div><div class="goal-grid reveal">${cards}</div>${unofficial()}`);
  }
  const STEP_TEXT = {
    zero: [
      ['run', { zh: '跑起第一个程序', en: 'Run your first program' }, { zh: '在浏览器里点一下就能运行，不用安装任何东西。先看到程序动起来。', en: 'Press Run in the browser with nothing to install. First see a program work.' }, 20],
      ['values', { zh: '变量、类型和文字', en: 'Values, types and text' }, { zh: '程序怎样记住东西、怎样处理文字。', en: 'How a program remembers things and handles text.' }, 60],
      ['flow', { zh: '条件和循环', en: 'Decisions and loops' }, { zh: '让程序根据情况走不同的路，并重复做事。', en: 'Let a program choose and repeat.' }, 90],
      ['data', { zh: '列表、字典和函数', en: 'Lists, dictionaries and functions' }, { zh: '组织数据，把步骤包成可以反复使用的函数。', en: 'Organise data and wrap steps into reusable functions.' }, 120],
      ['drill', { zh: '做练习，养成每天复习', en: 'Practise, and start a daily review' }, { zh: '先做题，做错的题会进入复习队列。之后每天花 10 分钟，系统在你快忘时再问你。', en: 'Try the questions. The ones you miss join your review queue, and ten minutes a day keeps them fresh.' }, 30],
      ['debug', { zh: '文件和调试', en: 'Files and debugging' }, { zh: '读懂报错，找到问题，处理真实的数据文件。', en: 'Read errors, find the problem and handle real data files.' }, 90],
      ['project', { zh: '做一个完整小项目', en: 'Write small programs on your own' }, { zh: '把学过的东西连起来，独立完成一件事。', en: 'The complete projects are in the Chinese handbook. In English, write small programs from a blank page and check them with the tests.' }, 120],
      ['next', { zh: '选下一门课', en: 'Choose what comes next' }, { zh: '想理解程序设计就学 Java，想学 AI 就读 AI 入门。', en: 'Java for program design, or AI Start for machine learning.' }, 5],
    ],
    exam: [
      ['diagnose', { zh: '先做一次小测，找出薄弱点', en: 'Sit a short test to find weak spots' }, { zh: '先测再学：只复习不会的，时间才够用。', en: 'Test before you revise, so the time goes where you need it.' }, 30],
      ['weak', { zh: '看该复习哪些章节', en: 'See what to revise' }, { zh: '按得分率排序。先读最低的两三章。', en: 'Sorted by score rate. Read the lowest two or three first.' }, 10],
      ['review', { zh: '把这门课加入每日复习', en: 'Add this course to your daily review' }, { zh: '每天做到期的卡片。分散复习比一次看完记得久。', en: 'Do the due cards each day. Spacing beats a single long read.' }, 15],
      ['drill', { zh: '按题型刷题', en: 'Drill by question type' }, { zh: '先做错过的章节，再做整门课。', en: 'First the chapters you lost marks on, then the whole course.' }, 120],
      ['sheet', { zh: '自己整理一页纸', en: 'Build your own one-page sheet' }, { zh: '对照速查表，把自己总出错的地方写下来。', en: 'Use the cheatsheet and write down what you keep getting wrong.' }, 30],
      ['mock', { zh: '限时做一套模拟卷', en: 'Sit a timed mock paper' }, { zh: '计时，不看资料。做完按评分标准打分。', en: 'Timed, no notes. Mark it against the rubric when done.' }, 90],
      ['redo', { zh: '重做丢分的题', en: 'Redo what lost marks' }, { zh: '隔一天再做一遍，而不是只看答案。', en: 'Redo them a day later rather than rereading the answer.' }, 45],
    ],
    paper: [
      ['guide', { zh: '先读手写指南', en: 'Read the by-hand guide' }, { zh: '怎样跟踪代码、怎样画内存图、要背哪些语法、手写常犯的错和怎样给自己打分。', en: 'How to trace code, draw memory, what syntax to memorise, common handwriting mistakes, and marking yourself.' }, 30],
      ['read', { zh: '学会读：预测输出', en: 'Read first: predict the output' }, { zh: '先练读代码：不运行，写出程序会打印什么。', en: 'Practise reading first: without running, write what a program prints.' }, 45],
      ['trace', { zh: '填跟踪表', en: 'Fill in trace tables' }, { zh: '一行一行执行，把每个变量的值写下来。', en: 'Run the code line by line and write down each variable.' }, 45],
      ['memory', { zh: '画内存图', en: 'Draw memory diagrams' }, { zh: '在标记的那一行，画出栈、堆、引用和指针的样子，再对照答案。', en: 'At the marked line, draw the stack, heap, references and pointers, then compare with the answer.' }, 45],
      ['write', { zh: '在纸上写代码', en: 'Write code on paper' }, { zh: '没有补全，没有运行。写完按评分标准打分，再敲进去运行。', en: 'No autocomplete, no running. Mark it against the rubric, then type it in and run it.' }, 90],
      ['mock', { zh: '限时手写一套卷', en: 'A timed paper by hand' }, { zh: '把上面的都放在一起，按时间写完。', en: 'Everything above together, against the clock.' }, 90],
    ],
    engineer: [
      ['labs', { zh: '做工程实验', en: 'Work through the labs' }, { zh: '用真实工具做调试、测试和代码审查，页面上是实际运行的输出。', en: 'Debugging, testing and code review with real tools; the page shows their actual output.' }, 90],
      ['project', { zh: '读一个完整工程', en: 'Read a complete project' }, { zh: '需求、接口、完整代码、调试过程和测试。', en: 'Requirements, interfaces, full source, debugging and tests.' }, 120],
      ['bugs', { zh: '找错练习', en: 'Find-the-bug drills' }, { zh: '读一段有问题的代码，说出错在哪里，再改好。', en: 'Read code with a fault in it, say what is wrong, then fix it.' }, 30],
      ['depth', { zh: '回到薄弱的基础', en: 'Go back to weak foundations' }, { zh: '用测验找到自己不熟的部分，只读那几章。', en: 'Use the quizzes to find what you do not know, and read only those chapters.' }, 60],
    ],
  };
  const handbook = (unit) => `${SITE}python-zero-to-practice/index.html#${unit}`;
  function stepsFor(g, data) {
    const c = g.course;
    const counts = {};
    (data?.questions || []).forEach((q) => { counts[q.kind] = (counts[q.kind] || 0) + 1; });
    const firstPaper = (type) => data?.papers?.find((p) => (type ? p.type === type : true));
    const target = {
      zero: (key) => {
        // the full handbook is in Chinese; the first-steps guide is the path in both languages, and goes further in Chinese
        const en = lang() === 'en';
        const guide = `${SITE}bridges/python-first-steps${en ? '' : '.zh'}.html`;
        return { run: `${guide}#first-program`, values: en ? `${guide}#values-names` : handbook('c02'), flow: en ? `${guide}#decisions` : handbook('c04'), data: en ? `${guide}#lists` : handbook('c07'), drill: '#/practice/python', debug: en ? `${guide}#read-errors` : handbook('c13'), project: en ? '#/practice/python?kind=write' : handbook('c17'), next: '#/route' }[key];
      },
      exam: (key) => ({ diagnose: firstPaper('diagnostic') ? `#/exam/${c}/${firstPaper('diagnostic').id}` : `#/practice/${c}`, weak: `#/practice/${c}`, review: '#/review', drill: `#/practice/${c}`, sheet: BY_ID[c].sheet?.[lang()] ? SITE + BY_ID[c].sheet[lang()] : null, mock: firstPaper('mock') ? `#/exam/${c}/${firstPaper('mock').id}` : `#/practice/${c}`, redo: `#/practice/${c}` }[key]),
      paper: (key) => ({ guide: `${SITE}bridges/${{ comp2017: 'paper-c', info1113: 'paper-java', python: 'paper-python', comp2123: 'paper-python' }[c]}${lang() === 'zh' ? '.zh' : ''}.html`, read: `#/practice/${c}?kind=predict`, trace: `#/practice/${c}?kind=trace`, memory: `#/practice/${c}?kind=memory`, write: `#/practice/${c}?kind=write`, mock: firstPaper('paper') ? `#/exam/${c}/${firstPaper('paper').id}` : `#/practice/${c}?kind=write` }[key]),
      engineer: (key) => ({ labs: `#/labs/${c}`, project: c === 'comp2017' ? `${SITE}projects/comp2017-log-analyzer.${lang() === 'zh' ? 'zh' : 'en'}.html` : null, bugs: `#/practice/${c}?kind=bug`, depth: `#/practice/${c}` }[key]),
    }[g.goal];
    const show = { read: !!counts.predict, trace: !!counts.trace, memory: !!counts.memory, write: !!counts.write, labs: !!data?.labs?.length, bugs: !!counts.bug, project: g.goal !== 'engineer' || c === 'comp2017', mock: g.goal === 'paper' ? !!firstPaper('paper') : g.goal === 'exam' ? !!firstPaper('mock') : true, diagnose: g.goal !== 'exam' || !!firstPaper('diagnostic') };
    return STEP_TEXT[g.goal].filter(([key]) => show[key] !== false).map(([key, title, why, min]) => ({ key, title, why, min, url: target(key) })).filter((s) => s.url);
  }
  function goalView(goal, course) {
    if (!STEP_TEXT[goal]) return hub.notFound();
    const pickCourse = goal !== 'zero' && !course;
    if (pickCourse) {
      // only offer what leads somewhere complete: papers for an exam, write questions by hand, labs at work
      const has = (id) => { const st = BY_ID[id]?.study; return !!st && (goal === 'exam' ? st.papers > 0 : goal === 'paper' ? st.kinds.write > 0 : st.labs > 0); };
      const options = (goal === 'paper' ? PAPER_LANGS : goal === 'engineer' ? [['comp2017', 'C'], ['info1113', 'Java'], ['comp2123', 'Python'], ['ml', 'AI']] : COURSE_IDS.filter((id) => BY_ID[id]).map((id) => [id, BY_ID[id].code])).filter(([id]) => has(id));
      const buttons = options.map(([id, name]) => {
        const c = BY_ID[id];
        return `<a class="panel route-card" href="#/goal/${goal}/${id}" style="--accent:${c.color}"><span class="icon-tile" style="--accent:${c.color}">${icon(c.icon)}</span><span><span class="code">${esc(name)}</span><b>${esc(L(c.title))}</b>${lang() === 'en' && !c.read.en ? `<small>${t('chineseChapters')}</small>` : ''}</span></a>`;
      }).join('');
      return frame('start', `${crumbs([t('navStart'), '#/start'], [t('goals')[goal][0]])}<div class="page-head"><div><h1>${esc(t('goals')[goal][0])}</h1><p>${t(goal === 'paper' || goal === 'engineer' ? 'choosePaper' : 'chooseCourse')}</p></div></div><div class="route-cards reveal">${buttons}</div>${unofficial()}`);
    }
    const render = (data) => {
      const g = { goal, course, done: routeDone(goal, course) };
      setGoal({ goal, course });
      const steps = stepsFor(g, data);
      const finished = steps.filter((s) => g.done[s.key]).length;
      const current = steps.find((s) => !g.done[s.key]);
      const list = steps.map((s, i) => `<li class="route-step${g.done[s.key] ? ' done' : ''}${s === current ? ' current' : ''}"><span class="step-no">${g.done[s.key] ? icon('check') : i + 1}</span><div><h3>${esc(L(s.title))}</h3><p>${esc(L(s.why))}</p><div class="step-actions"><a class="btn ${s === current ? 'primary' : 'ghost'} sm" href="${s.url}">${t('openStep')}</a><button type="button" class="btn ghost sm" data-step-done="${s.key}">${g.done[s.key] ? t('markUndo') : t('markDone')}</button><span class="muted">${esc(t('minutes')(s.min))}</span></div></div></li>`).join('');
      return frame('start', `${crumbs([t('navStart'), '#/start'], [t('goals')[goal][0]])}<div class="page-head"><div><h1>${esc(t('goals')[goal][0])}${course ? ` · ${esc(BY_ID[course].code)}` : ''}</h1><p>${esc(t('stepsDone')(finished, steps.length))}</p></div><a class="btn ghost sm" href="#/start">${t('changeGoal')}</a></div>
        ${current ? '' : `<div class="panel empty">${t('routeDone')}</div>`}<ol class="route-steps reveal">${list}</ol>${goal === 'zero' ? '' : unofficial()}`);
    };
    if (course) return withCourse(course, 'start', render);
    return render(null);
  }
  /* the hub's front page: the next step of the route in one click, and today's review */
  function resumeRoute() {
    const g = goalState();
    if (!g || !t('goals')[g.goal]) return '';
    const data = g.course ? ready(g.course) : null;
    if (g.course && !BY_ID[g.course]) return '';
    if (g.course && !data) { loadCourse(g.course).then(() => hub.refreshResume?.(), () => {}); return ''; }
    const steps = stepsFor(g, data);
    const done = routeDone(g.goal, g.course);
    const next = steps.find((x) => !done[x.key]);
    const name = `${t('goals')[g.goal][0]}${g.course ? ` · ${BY_ID[g.course].code}` : ''}`;
    const count = t('stepsDone')(steps.filter((x) => done[x.key]).length, steps.length);
    const route = next
      ? `<a class="resume resume-route" data-resume-route href="${esc(next.url)}"><small>${esc(t('resumeRoute'))} · ${esc(name)} · ${esc(count)}</small><b>${esc(t('nextStep'))}: ${esc(L(next.title))}</b>${icon('arrow')}</a>`
      : `<a class="resume resume-route" data-resume-route href="#/goal/${g.goal}${g.course ? `/${g.course}` : ''}"><small>${esc(name)}</small><b>${esc(t('routeDone'))}</b>${icon('arrow')}</a>`;
    const st = dueStats();
    const review = st.ready ? `<a class="resume resume-review" href="#/review"><small>${esc(t('reviewToday'))}</small><b>${esc(t('cardsReady')(st.ready))}</b>${icon('arrow')}</a>` : '';
    return route + review;
  }
  /* my learning: route, review, practice and reading in one panel */
  function glancePanel() {
    const rows = [];
    const g = goalState();
    if (g && t('goals')[g.goal] && (!g.course || BY_ID[g.course])) {
      const data = g.course ? ready(g.course) : null;
      if (g.course && !data) loadCourse(g.course).then(() => hub.refreshGlance?.(), () => {});
      const steps = stepsFor(g, data);
      const finished = steps.filter((x) => routeDone(g.goal, g.course)[x.key]).length;
      rows.push({ label: t('glanceRoute'), main: `${t('goals')[g.goal][0]}${g.course ? ` · ${BY_ID[g.course].code}` : ''}`, sub: steps.length ? t('stepsDone')(finished, steps.length) : '', rate: steps.length ? finished / steps.length : 0, href: `#/goal/${g.goal}${g.course ? `/${g.course}` : ''}` });
    }
    const st = dueStats();
    const review = { label: t('glanceReview'), main: t('glanceDue')(st.ready, st.all), sub: '', rate: null, href: '#/review' };
    const tried = {};
    Object.entries(attempts()).forEach(([key, a]) => { const cid = key.split('/')[0]; if (!BY_ID[cid]) return; tried[cid] ??= { n: 0, best: 0, marks: 0 }; tried[cid].n += 1; tried[cid].best += a.best ?? a.score ?? 0; tried[cid].marks += a.marks || 0; });
    Object.entries(tried).forEach(([cid, v]) => { const pct = v.marks ? Math.round((v.best / v.marks) * 100) : 0; rows.push({ label: t('glancePractice'), main: BY_ID[cid].code, sub: t('glanceScore')(v.n, pct), rate: v.marks ? v.best / v.marks : 0, href: `#/practice/${cid}` }); });
    const progress = store.get('leon-learn-progress', { courses: {} });
    Object.entries(progress.courses || {}).forEach(([cid, v]) => { const c = BY_ID[cid]; if (!c || !v.read?.length) return; rows.push({ label: t('glanceRead'), main: c.code, sub: t('glanceReadN')(v.read.length, c.chapters.length), rate: v.read.length / c.chapters.length, href: SITE + v.url }); });
    // review always shows once there is anything else to show, so "0 due" reads as news, not as a gap
    if (rows.length || st.all) rows.splice(g ? 1 : 0, 0, review);
    const list = rows.length ? `<ul class="glance-list">${rows.map((r) => `<li><span class="glance-label">${esc(r.label)}</span><span class="glance-main"><b>${esc(r.main)}</b>${r.sub ? `<small>${esc(r.sub)}</small>` : ''}</span>${r.rate == null ? '<span class="glance-bar empty"></span>' : `<span class="glance-bar" role="img" aria-label="${Math.round(r.rate * 100)}%"><i style="width:${Math.round(r.rate * 100)}%"></i></span>`}<a class="btn ghost sm" href="${r.href}">${esc(t('glanceOpen'))}</a></li>`).join('')}</ul>` : `<div class="empty">${esc(t('glanceEmpty'))}</div>`;
    return `<section class="panel glance" data-glance aria-labelledby="glance-title"><div class="panel-head"><h2 id="glance-title">${esc(t('glance'))}</h2></div>${list}</section>`;
  }
  /* the one-line prompt shown on the course list and my-learning pages */
  function goalBanner() {
    const g = goalState();
    if (!g) return `<a class="panel goal-banner" href="#/start"><b>${t('chooseGoal')}</b><span>${t('chooseGoalSub')}</span>${icon('arrow')}</a>`;
    const data = g.course ? ready(g.course) : null;
    if (g.course && !data) loadCourse(g.course).then(() => hub.refreshBanner?.(), () => {});
    const steps = stepsFor(g, data);
    const done = routeDone(g.goal, g.course);
    const next = steps.find((s) => !done[s.key]);
    return `<a class="panel goal-banner" href="#/goal/${g.goal}${g.course ? `/${g.course}` : ''}"><b>${t('resumeRoute')}</b><span>${esc(t('goals')[g.goal][0])}${g.course ? ` · ${esc(BY_ID[g.course].code)}` : ''}${next ? ` — ${t('nextStep')}: ${esc(L(next.title))}` : ''}</span>${icon('arrow')}</a>`;
  }

  /* ------------------------------------------------------------ practice lists */
  function practiceHome() {
    const tiles = COURSE_IDS.filter((id) => BY_ID[id]).map((id) => {
      const c = BY_ID[id];
      const tried = Object.keys(attempts()).filter((k) => k.startsWith(`${id}/`)).length;
      return `<a class="panel route-card" href="#/practice/${id}" style="--accent:${c.color}"><span class="icon-tile" style="--accent:${c.color}">${icon(c.icon)}</span><span><span class="code">${esc(c.code)}</span><b>${esc(L(c.title))}</b><small>${tried ? esc(t('qCount')(tried)) : ''}</small></span></a>`;
    }).join('');
    return frame('practice', `<div class="page-head"><div><h1>${t('practiceTitle')}</h1><p>${t('practiceSub')}</p></div><a class="btn ghost sm" href="#/review">${t('navReview')}</a></div>
      <div class="route-cards reveal">${tiles}</div>${unofficial()}`);
  }
  const query = () => Object.fromEntries(new URLSearchParams(location.hash.split('?')[1] || ''));
  function weakList(cid, data) {
    const all = attempts();
    const by = {};
    data.questions.forEach((q) => {
      const a = all[`${cid}/${q.id}`];
      if (!a) return;
      by[q.topic] ??= { score: 0, marks: 0 };
      by[q.topic].score += a.score;
      by[q.topic].marks += a.marks;
    });
    const rows = Object.entries(by).map(([topic, v]) => ({ topic, rate: v.marks ? v.score / v.marks : 0, ...v })).sort((a, b) => a.rate - b.rate).slice(0, 8);
    if (!rows.length) return `<div class="empty">${t('weakEmpty')}</div>`;
    return `<ul class="weak-list">${rows.map((r) => `<li><div class="weak-bar"><span style="width:${Math.round(r.rate * 100)}%"></span></div><b>${Math.round(r.rate * 100)}%</b><span class="weak-name">${esc(chapterTitle(cid, r.topic))}</span><a class="btn ghost sm" href="${chapterUrl(cid, r.topic)}">${t('chapterRead')}</a><a class="btn ghost sm" href="#/practice/${cid}?topic=${r.topic}">${t('weakPractice')}</a></li>`).join('')}</ul>`;
  }
  // the handbook has no chapter cards; its practice questions serve as the deck
  const deckSize = (c) => c.study.cards || Object.values(c.study.kinds).reduce((a, b) => a + b, 0);
  function practiceCourse(cid) {
    if (!BY_ID[cid]) return hub.notFound();
    return withCourse(cid, 'practice', (data) => {
      const c = BY_ID[cid];
      const q = query();
      const all = attempts();
      const kinds = [...new Set(data.questions.map((x) => x.kind))];
      const topics = c.chapters.filter((ch) => data.questions.some((x) => x.topic === ch.id));
      const list = data.questions.filter((x) => (!q.kind || x.kind === q.kind) && (!q.topic || x.topic === q.topic));
      const link = (kind, topic) => { const p = new URLSearchParams(); if (kind) p.set('kind', kind); if (topic) p.set('topic', topic); const s = p.toString(); return `#/practice/${cid}${s ? `?${s}` : ''}`; };
      const firstOpen = list.find((x) => !all[`${cid}/${x.id}`]) || list[0];
      const rows = list.slice(0, 200).map((x) => `<li><a href="#/practice/${cid}/${x.id}${q.kind || q.topic ? `?${new URLSearchParams({ ...(q.kind && { kind: q.kind }), ...(q.topic && { topic: q.topic }) })}` : ''}"><span class="q-title"><b>${esc(L(x.title))}</b><small>${esc(t('kinds')[x.kind] || x.kind)} · ${esc(chapterTitle(cid, x.topic))}</small></span>${attemptTag(all[`${cid}/${x.id}`])}</a></li>`).join('');
      const papers = data.papers.map((p) => { const st = store.get(paperKey(cid, p.id), null); return `<a class="panel route-card" href="#/exam/${cid}/${p.id}" style="--accent:${c.color}"><span class="icon-tile" style="--accent:${c.color}">${icon('quiz')}</span><span><b>${esc(L(p.title))}</b><small>${esc(t('examMins')(p.minutes))} · ${esc(t('qCount')(p.questions.length))}${st?.submitted ? ` · ${esc(t('examLast')(st.total, st.max))}` : ''}</small></span></a>`; }).join('');
      const labs = data.labs.length ? `<a class="btn ghost sm" href="#/labs/${cid}">${t('labsTitle')}</a>` : '';
      return frame('practice', `${crumbs([t('practiceTitle'), '#/practice'], [c.code])}<div class="page-head" style="--accent:${c.color}"><div><h1>${esc(L(c.title))}</h1><p>${esc(t('qCount')(data.questions.length))} · ${esc(t('cardsCount')(deckSize(c)))}${data.papers.length ? ` · ${esc(t('papersCount')(data.papers.length))}` : ''}</p></div>${labs}</div>
        ${papers ? `<section class="study-section"><h2>${t('examsTitle')}</h2><p class="muted">${t('examIntro')}</p><div class="route-cards">${papers}</div></section>` : ''}
        <section class="panel study-section-panel"><div class="panel-head"><h2>${t('weakTitle')}</h2><span class="muted">${t('weakSub')}</span></div>${weakList(cid, data)}</section>
        <section class="panel study-section-panel"><div class="toolbar"><div class="filters" role="group"><a class="fil${q.kind ? '' : ' on'}" href="${link('', q.topic)}">${t('kindsAll')}</a>${kinds.map((k) => `<a class="fil${q.kind === k ? ' on' : ''}" href="${link(k, q.topic)}">${esc(t('kinds')[k] || k)}</a>`).join('')}</div>
          <select class="study-select" data-topic-filter aria-label="${t('stageName')}"><option value="">${t('topicsAll')}</option>${topics.map((ch) => `<option value="${ch.id}"${q.topic === ch.id ? ' selected' : ''}>${esc(L(ch.title))}</option>`).join('')}</select>
          ${firstOpen ? `<a class="btn primary sm" href="#/practice/${cid}/${firstOpen.id}${q.kind || q.topic ? `?${new URLSearchParams({ ...(q.kind && { kind: q.kind }), ...(q.topic && { topic: q.topic }) })}` : ''}">${t('continueSet')}</a>` : ''}</div>
          ${rows ? `<ul class="q-list">${rows}</ul>` : `<div class="empty">${t('noQuestions')}</div>`}</section>${unofficial()}`);
    });
  }

  /* ------------------------------------------------------------ one question */
  let qs = null; // state of the question on screen: { key, stage, answer, ... }
  function neighbours(cid, data, qid) {
    const q = query();
    const list = data.questions.filter((x) => (!q.kind || x.kind === q.kind) && (!q.topic || x.topic === q.topic));
    const i = list.findIndex((x) => x.id === qid);
    const suffix = q.kind || q.topic ? `?${new URLSearchParams({ ...(q.kind && { kind: q.kind }), ...(q.topic && { topic: q.topic }) })}` : '';
    return { next: i >= 0 && list[i + 1] ? `#/practice/${cid}/${list[i + 1].id}${suffix}` : '', prev: i > 0 ? `#/practice/${cid}/${list[i - 1].id}${suffix}` : '', suffix, at: i + 1, of: list.length };
  }
  function promptHtml(q) {
    const parts = [];
    if (q.prompt) parts.push(`<div class="q-prompt">${para(L(q.prompt))}</div>`);
    if (q.question) parts.push(`<div class="q-prompt">${para(L(q.question))}</div>`);
    if (q.intro) parts.push(`<p class="muted">${esc(L(q.intro))}</p>`);
    if (q.code) parts.push(codeBlock(q.code));
    if (q.given_code) parts.push(`<h4>${t('given')}</h4>${codeBlock(q.given_code)}`);
    return parts.join('');
  }
  function memoryHtml(model) {
    const box = (v) => `<div class="mem-var"><span>${esc(v.name)}</span><b${v.points ? ' class="ptr"' : ''}>${esc(v.value)}${v.points ? ` <i>→ ${esc(v.points)}</i>` : ''}</b></div>`;
    const stack = (model.stack || []).map((f) => `<div class="mem-frame"><h5>${esc(f.frame)}</h5>${f.vars.map(box).join('')}</div>`).join('');
    const heap = (model.heap || []).map((b) => `<div class="mem-block"><h5>${esc(b.id)}</h5>${(b.cells || []).map(box).join('')}</div>`).join('');
    const data = (model.data || []).map(box).join('');
    return `<div class="mem-diagram"><section><h4>${lang() === 'zh' ? '栈' : 'Stack'}</h4>${stack}</section><section><h4>${lang() === 'zh' ? '堆' : 'Heap'}</h4>${heap || '<p class="muted">—</p>'}</section>${data ? `<section><h4>${lang() === 'zh' ? '静态数据' : 'Static data'}</h4>${data}</section>` : ''}</div>`;
  }
  function solutionHtml(q) {
    const parts = [];
    if (q.model_code) parts.push(`<h4>${t('model')}</h4>${codeBlock(q.model_code)}`);
    if (q.memory) parts.push(`<h4>${t('model')}</h4>${memoryHtml(q.memory)}`);
    if (q.solution) parts.push(`<h4>${t('solution')}</h4>${para(L(q.solution))}`);
    return parts.join('');
  }
  function rubricHtml(q, ticks = []) {
    if (!q.rubric) return '';
    return `<h4>${t('rubric')}</h4><ul class="rubric">${q.rubric.map((r, i) => `<li><label><input type="checkbox" data-rubric="${i}"${ticks.includes(i) ? ' checked' : ''}><span class="rubric-m">+${r.marks}</span><span>${inline(L(r.text))}</span></label></li>`).join('')}</ul>`;
  }
  const mistakesHtml = (q) => (q.mistakes?.length ? `<h4>${t('mistakes')}</h4><ul class="study-list">${q.mistakes.map((m) => `<li>${inline(L(m))}</li>`).join('')}</ul>` : '');
  function questionBody(cid, q) {
    const st = qs;
    const answerBox = (placeholder, rows = 6) => `<textarea class="study-answer" data-answer rows="${rows}" spellcheck="false" autocapitalize="off" autocomplete="off" autocorrect="off" placeholder="${esc(placeholder)}">${esc(st.answer || '')}</textarea>`;
    if (q.kind === 'predict') {
      if (st.stage === 0) return `<p class="q-instruction">${t('predictPrompt')}</p>${answerBox(t('predictHint'), Math.min(q.output.split('\n').length + 1, 12))}<div class="q-actions"><button type="button" class="btn primary" data-check>${t('check')}</button></div>`;
      const r = st.result;
      const lines = r.lines.map((l) => `<tr class="${l.ok ? 'ok' : 'bad'}"><td>${l.ok ? icon('check') : '✕'}</td><td><code>${esc(l.want) || '&nbsp;'}</code></td><td><code>${esc(l.got) || '&nbsp;'}</code></td></tr>`).join('');
      const walk = L(q.walk) || [];
      return `<div class="q-result"><strong>${esc(t('scored')(r.score, q.marks))}</strong></div><div class="study-trace" tabindex="0"><table class="diff"><thead><tr><th></th><th>${t('expected')}</th><th>${t('yours')}</th></tr></thead><tbody>${lines}</tbody></table></div>
        ${q.run && canRun(q.language) ? `<div class="q-actions"><button type="button" class="btn ghost sm" data-run-q>${t('runIt')}</button></div><div class="q-run" data-run-out hidden aria-live="polite"></div>` : ''}
        ${walk.length ? `<h4>${t('walk')}</h4><ol class="study-list">${walk.map((x) => `<li>${inline(x)}</li>`).join('')}</ol>` : ''}${q.trace ? `<h4>${t('traceT')}</h4>${traceTable(q.trace)}` : ''}`;
    }
    if (q.kind === 'worked') {
      const steps = L(q.steps);
      if (st.stage === 0) return `<p class="q-instruction">${t('workedPrompt')}</p>${answerBox('', 5)}<div class="q-actions"><button type="button" class="btn primary" data-reveal>${t('showMethod')}</button></div>`;
      const shown = steps.slice(0, st.stage).map((s, i) => `<li><p>${inline(s)}</p><label class="had"><input type="checkbox" data-had="${i}"${st.had?.includes(i) ? ' checked' : ''}>${t('hadStep')}</label></li>`).join('');
      const more = st.stage < steps.length;
      return `<h4>${t('strategy')}</h4>${para(L(q.strategy))}<ol class="study-list worked">${shown}</ol>${more ? `<div class="q-actions"><button type="button" class="btn primary" data-more>${t('nextStepBtn')}</button></div>` : `<h4>${t('answer')}</h4>${para(L(q.answer))}<h4>${t('sanity')}</h4>${para(L(q.sanity))}<div class="q-result" tabindex="-1"><strong>${esc(t('scored')(st.had?.length || 0, q.marks))}</strong></div>${st.recorded ? '' : `<div class="q-actions"><button type="button" class="btn primary" data-finish>${t('finishMark')}</button></div>`}`}`;
    }
    if (q.kind === 'mcq') {
      const chosen = st.chosen;
      const opts = optionOrder(q).map((i) => { const o = q.options[i]; return `<li class="${st.stage && o.correct ? 'ok' : ''}${st.stage && chosen === i && !o.correct ? ' bad' : ''}"><label><input type="radio" name="mcq" value="${i}"${chosen === i ? ' checked' : ''}${st.stage ? ' disabled' : ''}><span>${inline(L(o.text))}</span></label>${st.stage && o.why ? `<small>${inline(L(o.why))}</small>` : ''}</li>`; }).join('');
      return `<ul class="mcq">${opts}</ul>${st.stage ? `<div class="q-result"><strong>${t(markMcq(q, chosen) ? 'correct' : 'wrong')} · ${esc(t('scored')(markMcq(q, chosen), q.marks))}</strong></div>${solutionHtml(q)}` : `<div class="q-actions"><button type="button" class="btn primary" data-check>${t('check')}</button></div>`}`;
    }
    if (q.kind === 'numeric') {
      return `<div class="numeric"><input type="text" inputmode="decimal" data-answer value="${esc(st.answer || '')}" placeholder="${t('numberPlaceholder')}"${st.stage ? ' disabled' : ''}>${q.unit ? `<span>${esc(L(q.unit))}</span>` : ''}${q.tolerance ? `<small class="muted">${esc(t('toleranceNote')(q.tolerance))}</small>` : ''}</div>${st.stage ? `<div class="q-result"><strong>${t(markNumeric(q, st.answer) ? 'correct' : 'wrong')} · ${esc(t('scored')(markNumeric(q, st.answer), q.marks))}</strong></div><p>${t('answer')}: <b>${esc(q.answer)}</b></p>${solutionHtml(q)}` : `<div class="q-actions"><button type="button" class="btn primary" data-check>${t('check')}</button></div>`}`;
    }
    if (q.kind === 'trace') {
      const given = new Set(q.given || []);
      const cols = L(q.columns);
      const cell = (r, c) => {
        if (c === 0 || given.has(`${r},${c}`)) return `<td>${esc(q.rows[r][c])}</td>`;
        const value = st.cells?.[`${r},${c}`] ?? '';
        if (!st.stage) return `<td><input type="text" data-cell="${r},${c}" value="${esc(value)}" spellcheck="false" autocomplete="off" aria-label="${esc(cols[c])} ${r + 1}"></td>`;
        const ok = normCell(value) === normCell(q.rows[r][c]);
        return `<td class="${ok ? 'ok' : 'bad'}">${ok ? esc(value) : `<s>${esc(value) || '—'}</s> <b>${esc(q.rows[r][c])}</b>`}</td>`;
      };
      const table = `<div class="study-trace" tabindex="0"><table class="fill"><thead><tr>${cols.map((c) => `<th>${esc(c)}</th>`).join('')}</tr></thead><tbody>${q.rows.map((row, r) => `<tr>${row.map((_, c) => cell(r, c)).join('')}</tr>`).join('')}</tbody></table></div>`;
      return `<p class="q-instruction">${t('traceFill')}</p>${table}${st.stage ? `<div class="q-result"><strong>${esc(t('cellsRight')(st.result.right, st.result.total))} · ${esc(t('scored')(st.result.score, q.marks))}</strong></div>${solutionHtml(q)}` : `<div class="q-actions"><button type="button" class="btn primary" data-check>${t('check')}</button></div>`}`;
    }
    /* written answers: write, memory, short, bug, proof, design. Attempt first, then self-mark against the rubric. */
    const paper = q.kind === 'write' || q.kind === 'memory' || q.kind === 'proof' || q.kind === 'design';
    if (st.stage === 0) {
      return `${paper ? `<div class="paper-note"><b>${t('paperMode')}</b><p>${t('paperNote')}</p>${q.minutes ? `<div class="paper-timer"><span>${t('paperTimer')}: ${esc(t('minutes')(q.minutes))}</span><button type="button" class="btn ghost sm" data-timer>${st.timer ? t('timerRun') : t('startTimer')}</button><b data-clock>${st.timer ? '' : ''}</b></div>` : ''}</div>` : ''}<label class="q-label">${paper ? t('typeHere') : t('yourAnswer')}${answerBox('', q.kind === 'write' ? 14 : 6)}</label><div class="q-actions"><button type="button" class="btn primary" data-reveal>${t('reveal')}</button></div>`;
    }
    const score = (st.ticks || []).reduce((n, i) => n + q.rubric[i].marks, 0);
    return `${st.answer ? `<h4>${t('yourAnswer')}</h4>${codeBlock(st.answer)}` : ''}${solutionHtml(q)}${rubricHtml(q, st.ticks || [])}<div class="q-result"><strong data-score>${esc(t('yourScore'))}: ${esc(t('scored')(score, q.marks))}</strong></div>${mistakesHtml(q)}
      ${q.tests && canRun(q.language) ? `<h4>${t('runTests')}</h4><textarea class="study-answer" data-typed rows="12" spellcheck="false" autocapitalize="off" autocomplete="off" autocorrect="off">${esc(st.typed ?? st.answer ?? q.starter ?? '')}</textarea><div class="q-actions"><button type="button" class="btn ghost" data-run-tests>${t('runIt')}</button></div><div class="q-run" data-run-out hidden aria-live="polite"></div>` : ''}`;
  }
  function questionView(cid, qid) {
    if (!BY_ID[cid]) return hub.notFound();
    return withCourse(cid, 'practice', (data) => {
      const q = data.questions.find((x) => x.id === qid);
      if (!q) return hub.notFound();
      const key = `${cid}/${qid}`;
      if (!qs || qs.key !== key) qs = { key, stage: 0, answer: '', had: [], ticks: [], cells: {} };
      const c = BY_ID[cid];
      const nav = neighbours(cid, data, qid);
      const canAdd = !AUTO.has(q.kind) || qs.stage;
      return frame('practice', `${crumbs([t('practiceTitle'), '#/practice'], [c.code, `#/practice/${cid}${nav.suffix}`], [`${nav.at} / ${nav.of}`])}
        <article class="panel q-panel reveal" style="--accent:${c.color}"><header><div class="tags">${badge(q)}</div><h1>${esc(L(q.title))}</h1><a class="q-chapter" href="${chapterUrl(cid, q.topic)}">${esc(chapterTitle(cid, q.topic))} ↗</a></header>
        ${promptHtml(q)}<div data-q-body>${questionBody(cid, q)}</div>
        <footer class="q-foot">${nav.prev ? `<a class="btn ghost sm" href="${nav.prev}">${t('prev')}</a>` : ''}<a class="btn ghost sm" href="#/practice/${cid}${nav.suffix}">${t('backList')}</a>${canAdd ? `<button type="button" class="btn ghost sm" data-add-q${inQueue(`q:${key}`) ? ' disabled' : ''}>${inQueue(`q:${key}`) ? t('addedReview') : t('addReview')}</button>` : ''}${nav.next ? `<a class="btn primary sm" href="${nav.next}">${t('next')}</a>` : ''}</footer></article>${unofficial()}`);
    });
  }
  function redrawQuestion(cid, q) {
    const body = hub.app.querySelector('[data-q-body]');
    if (body) body.innerHTML = questionBody(cid, q);
  }
  function runBox(box, html) { box.hidden = false; box.innerHTML = html; }
  function wireQuestion(cid, qid) {
    const q = ready(cid)?.questions.find((x) => x.id === qid);
    const root = hub.app.querySelector('.q-panel');
    if (!q || !root) return;
    const key = `${cid}/${qid}`;
    let clock;
    const stopClock = () => clearInterval(clock);
    hub.onLeave(stopClock);
    const save = (score, marks, { queue = true, sameTry = false } = {}) => {
      setAttempt(key, score, marks, { sameTry });
      if (!queue) return;
      if (score < marks) enqueue([`q:${key}`]);
      else {
        // earned full marks while self-marking: a card that has not been studied yet can leave the queue
        const s = srs();
        if (s[`q:${key}`]?.fresh) { delete s[`q:${key}`]; setSrs(s); }
      }
    };
    const focusResult = () => { const target = root.querySelector('[data-q-body] .q-result, [data-q-body] h4, [data-q-body] [data-rubric]'); if (target) { if (!target.matches('input')) target.setAttribute('tabindex', '-1'); target.focus({ preventScroll: false }); } };
    // the paper timer carries on across a re-render (language or theme change)
    const startClock = () => {
      const show = root.querySelector('[data-clock]');
      const tick = () => { const sec = Math.floor((now() - qs.timer) / 1000); if (show) show.textContent = `${Math.floor(sec / 60)}:${String(sec % 60).padStart(2, '0')}`; };
      tick();
      clock = setInterval(tick, 1000);
    };
    if (qs.timer && root.querySelector('[data-clock]')) startClock();
    root.addEventListener('input', (e) => {
      if (e.target.matches('[data-answer]')) qs.answer = e.target.value;
      if (e.target.matches('[data-typed]')) qs.typed = e.target.value;
      if (e.target.matches('[data-cell]')) qs.cells[e.target.dataset.cell] = e.target.value;
    });
    root.addEventListener('change', (e) => {
      if (e.target.name === 'mcq') qs.chosen = Number(e.target.value);
      if (e.target.matches('[data-had]')) {
        const i = Number(e.target.dataset.had);
        qs.had = e.target.checked ? [...new Set([...qs.had, i])] : qs.had.filter((x) => x !== i);
        if (qs.recorded) { save(qs.had.length, q.marks, { sameTry: true }); }
        redrawQuestion(cid, q);
      }
      if (e.target.matches('[data-rubric]')) {
        const i = Number(e.target.dataset.rubric);
        qs.ticks = e.target.checked ? [...new Set([...qs.ticks, i])] : qs.ticks.filter((x) => x !== i);
        const score = qs.ticks.reduce((n, k) => n + q.rubric[k].marks, 0);
        root.querySelector('[data-score]').textContent = `${t('yourScore')}: ${t('scored')(score, q.marks)}`;
        save(score, q.marks, { sameTry: true });
      }
    });
    root.addEventListener('click', async (e) => {
      if (e.target.closest('[data-check]')) {
        if (q.kind === 'predict') { qs.result = markPredict(q, qs.answer); save(qs.result.score, q.marks); }
        if (q.kind === 'mcq') { if (qs.chosen == null) return; save(markMcq(q, qs.chosen), q.marks); }
        if (q.kind === 'numeric') save(markNumeric(q, qs.answer), q.marks);
        if (q.kind === 'trace') { qs.result = markTrace(q, qs.cells); save(qs.result.score, q.marks); }
        qs.stage = 1;
        redrawQuestion(cid, q);
        focusResult();
        return;
      }
      if (e.target.closest('[data-reveal]')) {
        stopClock();
        qs.stage = 1;
        if (q.rubric) save(0, q.marks, { queue: false });
        redrawQuestion(cid, q);
        focusResult();
        return;
      }
      if (e.target.closest('[data-more]')) { qs.stage += 1; redrawQuestion(cid, q); hub.app.querySelector('[data-more], [data-finish]')?.focus(); return; }
      if (e.target.closest('[data-finish]')) { qs.recorded = true; save(qs.had.length, q.marks); redrawQuestion(cid, q); return; }
      if (e.target.closest('[data-timer]')) {
        if (qs.timer) return;
        qs.timer = now();
        startClock();
        return;
      }
      if (e.target.closest('[data-add-q]')) {
        enqueue([`q:${key}`]);
        const b = e.target.closest('[data-add-q]');
        b.textContent = t('addedReview');
        b.disabled = true;
        return;
      }
      const runQ = e.target.closest('[data-run-q]');
      if (runQ) {
        const box = root.querySelector('[data-run-out]');
        runBox(box, `<p>${t('running')}</p>`);
        const { run } = await import(`${SITE}assets/runner/run.js`);
        const r = await run({ language: q.language, code: q.code });
        runBox(box, `<h4>${t('ranOut')}</h4><pre class="study-code">${esc(r.stdout + (r.stderr || ''))}</pre>`);
        if (r.status !== 'ok') {
          const { explainNode } = await import(`${SITE}assets/runner/explain.js`);
          const note = explainNode(r, { language: q.language, lang: lang() });
          if (note) box.querySelector('h4').after(note);
        }
        return;
      }
      const runT = e.target.closest('[data-run-tests]');
      if (runT) {
        const box = root.querySelector('[data-run-out]');
        runBox(box, `<p>${t('running')}</p>`);
        const { run } = await import(`${SITE}assets/runner/run.js`);
        const typed = qs.typed ?? qs.answer ?? '';
        const r = await run({ language: q.language, code: typed, tests: q.tests });
        const pass = r.status === 'ok' && (q.expected == null || r.stdout.replace(/\n$/, '') === q.expected.replace(/\n$/, ''));
        runBox(box, `<div class="q-result ${pass ? 'pass' : 'fail'}"><strong>${t(pass ? 'testsPass' : 'testsFail')}</strong></div><pre class="study-code">${esc((r.stdout || '') + (r.stderr || ''))}</pre>`);
        // what went wrong, in plain words, with the line in what the reader typed (the tests are appended after it)
        if (!pass) {
          const { explainNode } = await import(`${SITE}assets/runner/explain.js`);
          const note = explainNode(r, { language: q.language, lang: lang(), ownLines: typed.split('\n').length });
          if (note) box.querySelector('.q-result').after(note);
        }
      }
    });
  }

  /* ------------------------------------------------------------ mock papers */
  let timerHandle = null;
  const fmtTime = (ms) => { const s = Math.max(0, Math.ceil(ms / 1000)); return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`; };
  function paperState(cid, pid) { return store.get(paperKey(cid, pid), null); }
  function paperQuestions(data, paper) { return paper.questions.map((id) => data.questions.find((x) => x.id === id)).filter(Boolean); }
  function paperScore(questions, st) {
    let total = 0; let max = 0;
    const per = {};
    questions.forEach((q) => {
      const a = st.answers[q.id] || {};
      let score;
      if (q.kind === 'predict') score = markPredict(q, a.text || '').score;
      else if (q.kind === 'mcq') score = a.choice == null ? 0 : markMcq(q, a.choice);
      else if (q.kind === 'numeric') score = markNumeric(q, a.text);
      else if (q.kind === 'trace') score = markTrace(q, a.cells || {}).score;
      else if (q.kind === 'worked') score = (a.ticks || []).length;
      else score = (a.ticks || []).reduce((n, i) => n + q.rubric[i].marks, 0);
      total += score; max += q.marks;
      per[q.id] = score;
    });
    return { total, max, per };
  }
  function examQuestion(q, a, i, done) {
    const head = `<header><span class="exam-no">${i + 1}</span><div class="tags">${badge(q)}</div></header><h3>${esc(L(q.title))}</h3>${promptHtml(q)}`;
    const box = (rows, val = a.text || '') => `<textarea class="study-answer" data-exam-text="${q.id}" rows="${rows}" aria-label="${esc(t('yourAnswer'))}: ${esc(L(q.title))}" spellcheck="false" autocapitalize="off" autocomplete="off" autocorrect="off"${done ? ' readonly' : ''}>${esc(val)}</textarea>`;
    if (!done) {
      let input;
      if (q.kind === 'mcq') input = `<ul class="mcq">${optionOrder(q).map((k) => `<li><label><input type="radio" name="x-${q.id}" data-exam-choice="${q.id}" value="${k}"${a.choice === k ? ' checked' : ''}><span>${inline(L(q.options[k].text))}</span></label></li>`).join('')}</ul>`;
      else if (q.kind === 'numeric') input = `<div class="numeric"><input type="text" inputmode="decimal" data-exam-text="${q.id}" aria-label="${esc(t('yourAnswer'))}: ${esc(L(q.title))}" value="${esc(a.text || '')}" placeholder="${t('numberPlaceholder')}">${q.unit ? `<span>${esc(L(q.unit))}</span>` : ''}</div>`;
      else if (q.kind === 'trace') {
        const given = new Set(q.given || []);
        input = `<div class="study-trace" tabindex="0"><table class="fill"><thead><tr>${L(q.columns).map((c) => `<th>${esc(c)}</th>`).join('')}</tr></thead><tbody>${q.rows.map((row, r) => `<tr>${row.map((v, c) => (c === 0 || given.has(`${r},${c}`) ? `<td>${esc(v)}</td>` : `<td><input type="text" data-exam-cell="${q.id}" data-rc="${r},${c}" aria-label="${esc(L(q.columns)[c])} ${r + 1}" value="${esc(a.cells?.[`${r},${c}`] || '')}" spellcheck="false" autocomplete="off"></td>`)).join('')}</tr>`).join('')}</tbody></table></div>`;
      } else input = box(q.kind === 'write' ? 12 : q.kind === 'predict' ? Math.min(q.output.split('\n').length + 1, 10) : 6);
      return `<section class="panel exam-q" id="q-${q.id}">${head}${input}</section>`;
    }
    let result;
    if (AUTO.has(q.kind)) {
      if (q.kind === 'predict') { const m = markPredict(q, a.text || ''); result = `<div class="q-result"><strong>${t('examAuto')} · ${esc(t('scored')(m.score, q.marks))}</strong></div><h4>${t('yourAnswer')}</h4>${codeBlock(a.text || '')}<h4>${t('expected')}</h4>${codeBlock(q.output)}`; }
      if (q.kind === 'mcq') result = `<ul class="mcq">${optionOrder(q).map((k) => { const o = q.options[k]; return `<li class="${o.correct ? 'ok' : ''}${a.choice === k && !o.correct ? ' bad' : ''}"><label><input type="radio" disabled${a.choice === k ? ' checked' : ''}><span>${inline(L(o.text))}</span></label>${o.why ? `<small>${inline(L(o.why))}</small>` : ''}</li>`; }).join('')}</ul><div class="q-result"><strong>${t('examAuto')} · ${esc(t('scored')(a.choice == null ? 0 : markMcq(q, a.choice), q.marks))}</strong></div>${solutionHtml(q)}`;
      if (q.kind === 'numeric') result = `<p>${t('yourAnswer')}: <b>${esc(a.text || '—')}</b> · ${t('answer')}: <b>${esc(q.answer)}</b></p><div class="q-result"><strong>${t('examAuto')} · ${esc(t('scored')(markNumeric(q, a.text), q.marks))}</strong></div>${solutionHtml(q)}`;
      if (q.kind === 'trace') { const m = markTrace(q, a.cells || {}); const given = new Set(q.given || []); result = `<div class="study-trace" tabindex="0"><table class="fill"><thead><tr>${L(q.columns).map((c) => `<th>${esc(c)}</th>`).join('')}</tr></thead><tbody>${q.rows.map((row, r) => `<tr>${row.map((v, c) => { if (c === 0 || given.has(`${r},${c}`)) return `<td>${esc(v)}</td>`; const got = a.cells?.[`${r},${c}`] ?? ''; const ok = normCell(got) === normCell(v); return `<td class="${ok ? 'ok' : 'bad'}">${ok ? esc(got) : `<s>${esc(got) || '—'}</s> <b>${esc(v)}</b>`}</td>`; }).join('')}</tr>`).join('')}</tbody></table></div><div class="q-result"><strong>${t('examAuto')} · ${esc(t('cellsRight')(m.right, m.total))} · ${esc(t('scored')(m.score, q.marks))}</strong></div>${solutionHtml(q)}`; }
    } else if (q.kind === 'worked') {
      const steps = L(q.steps);
      result = `<h4>${t('yourAnswer')}</h4>${codeBlock(a.text || '')}<p class="muted">${t('examSelf')}</p><h4>${t('strategy')}</h4>${para(L(q.strategy))}<ol class="study-list worked">${steps.map((s, k) => `<li><p>${inline(s)}</p><label class="had"><input type="checkbox" data-exam-tick="${q.id}" value="${k}"${(a.ticks || []).includes(k) ? ' checked' : ''}>${t('hadStep')}</label></li>`).join('')}</ol><h4>${t('answer')}</h4>${para(L(q.answer))}`;
    } else {
      result = `<h4>${t('yourAnswer')}</h4>${codeBlock(a.text || '')}<p class="muted">${t('examSelf')}</p>${solutionHtml(q)}<h4>${t('rubric')}</h4><ul class="rubric">${q.rubric.map((r, k) => `<li><label><input type="checkbox" data-exam-tick="${q.id}" value="${k}"${(a.ticks || []).includes(k) ? ' checked' : ''}><span class="rubric-m">+${r.marks}</span><span>${inline(L(r.text))}</span></label></li>`).join('')}</ul>${mistakesHtml(q)}`;
    }
    return `<section class="panel exam-q" id="q-${q.id}">${head}${result}</section>`;
  }
  function examView(cid, pid) {
    if (!BY_ID[cid]) return hub.notFound();
    return withCourse(cid, 'practice', (data) => {
      const paper = data.papers.find((p) => p.id === pid);
      if (!paper) return hub.notFound();
      const c = BY_ID[cid];
      const questions = paperQuestions(data, paper);
      const st = paperState(cid, pid);
      const head = `${crumbs([t('practiceTitle'), '#/practice'], [c.code, `#/practice/${cid}`], [L(paper.title)])}`;
      if (!st) {
        const total = questions.reduce((n, q) => n + q.marks, 0);
        return frame('practice', `${head}<article class="panel q-panel" style="--accent:${c.color}"><header><h1>${esc(L(paper.title))}</h1></header><p>${esc(t('examMins')(paper.minutes))} · ${esc(t('qCount')(questions.length))} · ${esc(t('marks')(total))}</p>${paper.note ? para(L(paper.note)) : ''}<p>${t('examIntro')}</p><p>${t('examPaperNote')}</p>${unofficial()}<div class="q-actions"><button type="button" class="btn primary lg" data-exam-begin>${t('examStart')}</button></div></article>`);
      }
      if (!st.submitted) {
        return frame('practice', `<div class="exam-bar"><b>${esc(L(paper.title))}</b><span data-exam-clock aria-live="off">${t('timeLeft')} ${fmtTime(st.ends - now())}</span><button type="button" class="btn primary sm" data-exam-submit>${t('examSubmit')}</button></div><div class="exam-paper">${questions.map((q, i) => examQuestion(q, st.answers[q.id] || {}, i, false)).join('')}</div><div class="q-actions"><button type="button" class="btn primary lg" data-exam-submit>${t('examSubmit')}</button></div>`);
      }
      const score = paperScore(questions, st);
      const byTopic = {};
      questions.forEach((q) => { byTopic[q.topic] ??= { s: 0, m: 0 }; byTopic[q.topic].s += score.per[q.id]; byTopic[q.topic].m += q.marks; });
      const topics = Object.entries(byTopic).sort((a, b) => a[1].s / a[1].m - b[1].s / b[1].m).map(([id, v]) => `<li><div class="weak-bar"><span style="width:${Math.round((v.s / v.m) * 100)}%"></span></div><b>${v.s}/${v.m}</b><span class="weak-name">${esc(chapterTitle(cid, id))}</span><a class="btn ghost sm" href="${chapterUrl(cid, id)}">${t('chapterRead')}</a></li>`).join('');
      return frame('practice', `${head}<section class="panel q-panel" style="--accent:${c.color}"><header><span class="muted">${t('examResult')}</span><h1 data-exam-total>${esc(t('examTotal')(score.total, score.max))}</h1></header><h4>${t('examByTopic')}</h4><ul class="weak-list">${topics}</ul><div class="q-actions"><button type="button" class="btn ghost" data-exam-missed>${t('examAddMissed')}</button><button type="button" class="btn ghost" data-exam-again>${t('examAgain')}</button></div>${unofficial()}</section><div class="exam-paper">${questions.map((q, i) => examQuestion(q, st.answers[q.id] || {}, i, true)).join('')}</div>`);
    });
  }
  function wireExam(cid, pid) {
    const app = hub.app;
    const data = ready(cid);
    const paper = data?.papers.find((p) => p.id === pid);
    if (!paper) return;
    const questions = paperQuestions(data, paper);
    const key = paperKey(cid, pid);
    let st = store.get(key, null);
    const save = () => store.set(key, st);
    clearInterval(timerHandle);
    hub.onLeave(() => clearInterval(timerHandle));
    const clock = app.querySelector('[data-exam-clock]');
    if (clock && st && !st.submitted) {
      timerHandle = setInterval(() => {
        const left = st.ends - now();
        clock.textContent = left > 0 ? `${t('timeLeft')} ${fmtTime(left)}` : t('timeUp');
        clock.classList.toggle('over', left <= 0);
        clock.classList.toggle('near', left > 0 && left < 300000);
      }, 1000);
    }
    const root = app.querySelector('main');
    root.addEventListener('input', (e) => {
      if (!st) return;
      const id = e.target.dataset.examText;
      if (id) { st.answers[id] = { ...st.answers[id], text: e.target.value }; save(); }
      const cell = e.target.dataset.examCell;
      if (cell) { const a = st.answers[cell] || {}; a.cells = { ...(a.cells || {}), [e.target.dataset.rc]: e.target.value }; st.answers[cell] = a; save(); }
    });
    root.addEventListener('change', (e) => {
      if (!st) return;
      const id = e.target.dataset.examChoice;
      if (id) { st.answers[id] = { ...st.answers[id], choice: Number(e.target.value) }; save(); }
      const tick = e.target.dataset.examTick;
      if (tick) {
        const a = st.answers[tick] || {};
        const v = Number(e.target.value);
        a.ticks = e.target.checked ? [...new Set([...(a.ticks || []), v])] : (a.ticks || []).filter((x) => x !== v);
        st.answers[tick] = a;
        const score = paperScore(questions, st);
        st.total = score.total; st.max = score.max;
        save();
        const head = app.querySelector('[data-exam-total]');
        if (head) head.textContent = t('examTotal')(score.total, score.max);
        recordPaper(score);
      }
    });
    const recordPaper = (score) => { questions.forEach((q) => setAttempt(`${cid}/${q.id}`, score.per[q.id], q.marks)); };
    root.addEventListener('click', (e) => {
      if (e.target.closest('[data-exam-begin]')) {
        st = { start: now(), ends: now() + paper.minutes * 60000, answers: {}, submitted: false };
        save();
        hub.render();
        return;
      }
      if (e.target.closest('[data-exam-submit]')) {
        if (!window.confirm(t('examConfirm'))) return;
        st.submitted = true;
        st.finished = now();
        const score = paperScore(questions, st);
        st.total = score.total; st.max = score.max;
        save();
        recordPaper(score);
        clearInterval(timerHandle);
        hub.render();
        window.scrollTo(0, 0);
        return;
      }
      if (e.target.closest('[data-exam-again]')) {
        store.remove(key);
        hub.render();
        window.scrollTo(0, 0);
        return;
      }
      const missed = e.target.closest('[data-exam-missed]');
      if (missed) {
        const score = paperScore(questions, st);
        enqueue(questions.filter((q) => score.per[q.id] < q.marks).map((q) => `q:${cid}/${q.id}`));
        missed.textContent = t('examDone');
        missed.disabled = true;
      }
    });
  }

  /* ------------------------------------------------------------ review queue */
  let session = null;
  function dueStats() {
    const s = srs();
    const t0 = now();
    let due = 0; let fresh = 0;
    const today = store.get('leon-learn-srs-day', { date: '', fresh: 0 });
    Object.values(s).forEach((c) => { if (c.fresh) fresh += 1; else if (c.due <= t0) due += 1; });
    const leftNew = Math.max(0, NEW_PER_DAY - (today.date === dayStamp() ? today.fresh : 0));
    return { due, fresh, leftNew, all: Object.keys(s).length, ready: due + Math.min(fresh, leftNew) };
  }
  function reviewHome() {
    const st = dueStats();
    const s = srs();
    const missed = (id) => Object.keys(s).filter((k) => k.startsWith(`q:${id}/`)).length;
    const rows = COURSE_IDS.filter((id) => BY_ID[id]).map((id) => {
      const c = BY_ID[id];
      const usesQuestions = !c.study.cards;
      const inDeck = Object.keys(s).filter((k) => k.startsWith(usesQuestions ? `q:${id}/` : `${id}/`)).length;
      const totalCards = deckSize(c);
      if (!totalCards) return '';
      return `<li style="--accent:${c.color}"><span class="icon-tile" style="--accent:${c.color}">${icon(c.icon)}</span><span class="deck-name"><b>${esc(c.code)}</b><small>${esc(L(c.title))}</small></span><span class="muted deck-count">${esc(t('inDeck')(inDeck, totalCards))}${!usesQuestions && missed(id) ? ` · ${esc(t('missedInDeck')(missed(id)))}` : ''}</span>${usesQuestions ? '' : `<button type="button" class="btn ghost sm" data-deck-read="${id}">${t('addRead')}</button>`}<button type="button" class="btn ghost sm" data-deck-all="${id}">${t('addAll')}</button></li>`;
    }).join('');
    return frame('review', `<div class="page-head"><div><h1>${t('reviewTitle')}</h1><p>${t('reviewSub')}</p></div></div>
      <section class="panel review-top reveal"><dl class="review-stats"><div><dt>${t('dueNow')}</dt><dd>${st.due}</dd></div><div><dt>${t('newCards')}</dt><dd>${Math.min(st.fresh, st.leftNew)}<small>/${st.fresh}</small></dd></div><div><dt>${t('allCards')}</dt><dd>${st.all}</dd></div></dl>${st.ready ? `<button type="button" class="btn primary lg" data-review-start>${t('startReview')} ${icon('arrow')}</button>` : `<p class="muted">${st.all ? t('nothingDue') : t('reviewEmpty')}</p>`}<p class="muted review-limit">${esc(t('newLimit')(NEW_PER_DAY))}</p></section>
      <section class="panel study-section-panel"><div class="panel-head"><h2>${t('addDeck')}</h2></div><ul class="deck-list">${rows}</ul></section>`);
  }
  async function cardContent(key) {
    if (key.startsWith('q:')) {
      const [cid, qid] = key.slice(2).split('/');
      const data = await loadCourse(cid);
      const q = data.questions.find((x) => x.id === qid);
      return q ? { cid, topic: q.topic, kind: 'question', q } : null;
    }
    const [cid, id] = key.split('/');
    const data = await loadCourse(cid);
    const card = data.cards.find((x) => x.id === id);
    return card ? { cid, topic: card.topic, kind: 'card', card } : null;
  }
  function buildSession() {
    const s = srs();
    const t0 = now();
    const today = store.get('leon-learn-srs-day', { date: '', fresh: 0 });
    const leftNew = Math.max(0, NEW_PER_DAY - (today.date === dayStamp() ? today.fresh : 0));
    const due = Object.entries(s).filter(([, c]) => !c.fresh && c.due <= t0).sort((a, b) => a[1].due - b[1].due).map(([k]) => k);
    const fresh = Object.entries(s).filter(([, c]) => c.fresh).sort((a, b) => a[1].added - b[1].added).slice(0, leftNew).map(([k]) => k);
    return { queue: [...due, ...fresh], total: due.length + fresh.length, done: 0, flipped: false, content: null };
  }
  function sessionView() {
    if (!session) session = buildSession();
    if (!session.queue.length) {
      const n = session.done;
      session = null;
      return frame('review', `<div class="panel q-panel" style="text-align:center"><h1>${t('sessionDone')}</h1><p>${esc(t('sessionStats')(n))}</p><div class="q-actions" style="justify-content:center"><a class="btn ghost" href="#/practice">${t('navPractice')}</a><a class="btn primary" href="#/start">${t('navStart')}</a></div></div>`);
    }
    const key = session.queue[0];
    if (!srs()[key]) { // cleared or restored elsewhere while this round was open
      session.queue.shift();
      session.content = null;
      return sessionView();
    }
    if (!session.content || session.contentKey !== key) {
      cardContent(key).then((c) => {
        if (!session) return;
        if (!c) { const s = srs(); delete s[key]; setSrs(s); session.queue.shift(); }
        else { session.content = c; session.contentKey = key; session.flipped = false; }
        hub.render();
      }).catch(() => { hub.app.querySelector('[data-load]')?.replaceChildren(t('loadFail')); });
      return frame('review', `<div class="panel empty" data-load>${t('loading')}</div>`);
    }
    const c = session.content;
    const course = BY_ID[c.cid];
    const prog = `${esc(t('cardOf')(session.done + 1, session.total))} · ${esc(course.code)} · ${esc(chapterTitle(c.cid, c.topic))}`;
    let front; let back;
    if (c.kind === 'card') {
      front = para(L(c.card.q));
      back = para(L(c.card.a));
    } else {
      const q = c.q;
      front = `<div class="tags">${badge(q)}</div><h2>${esc(L(q.title))}</h2>${promptHtml(q)}`;
      back = q.kind === 'predict' ? `<h4>${t('expected')}</h4>${codeBlock(q.output)}`
        : q.kind === 'worked' ? `<h4>${t('strategy')}</h4>${para(L(q.strategy))}<ol class="study-list">${L(q.steps).map((s) => `<li>${inline(s)}</li>`).join('')}</ol><h4>${t('answer')}</h4>${para(L(q.answer))}`
          : q.kind === 'mcq' ? `<ul class="mcq">${optionOrder(q).map((k) => q.options[k]).map((o) => `<li class="${o.correct ? 'ok' : ''}"><span>${inline(L(o.text))}</span>${o.why ? `<small>${inline(L(o.why))}</small>` : ''}</li>`).join('')}</ul>`
            : q.kind === 'numeric' ? `<p>${t('answer')}: <b>${esc(q.answer)}</b></p>${solutionHtml(q)}`
              : q.kind === 'trace' ? `<div class="study-trace" tabindex="0"><table class="fill"><thead><tr>${L(q.columns).map((x) => `<th>${esc(x)}</th>`).join('')}</tr></thead><tbody>${q.rows.map((row) => `<tr>${row.map((v) => `<td>${esc(v)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>${solutionHtml(q)}`
                : `${solutionHtml(q)}${q.rubric ? `<ul class="study-list">${q.rubric.map((r) => `<li>+${r.marks} ${inline(L(r.text))}</li>`).join('')}</ul>` : ''}`;
    }
    const s = srs();
    const state = s[key].fresh ? null : s[key];
    const when = (rating) => F().review(state, rating, now()).days;
    const buttons = [[F().AGAIN, 'again'], [F().HARD, 'hard'], [F().GOOD, 'good'], [F().EASY, 'easy']];
    return frame('review', `<div class="review-progress"><span>${prog}</span><i style="width:${Math.round((session.done / Math.max(1, session.total)) * 100)}%"></i></div>
      <article class="panel q-panel review-card" style="--accent:${course.color}"><div class="review-front">${front}</div>
      ${session.flipped ? `<div class="review-back">${back}</div><div class="rate-row">${buttons.map(([r, name]) => `<button type="button" class="rate ${name}" data-rate="${r}"><b>${t(name)}</b><small>${esc(r === F().AGAIN ? t('days')(0) : t('days')(when(r)))}</small></button>`).join('')}</div>` : `<div class="q-actions"><button type="button" class="btn primary" data-flip>${t('showAnswer')}</button></div>`}
      <a class="q-chapter" href="${chapterUrl(c.cid, c.topic)}">${esc(chapterTitle(c.cid, c.topic))} ↗</a></article>`);
  }
  function wireReview() {
    const root = hub.app.querySelector('main');
    root.addEventListener('click', async (e) => {
      if (e.target.closest('[data-review-start]')) { session = buildSession(); location.hash = '#/review/run'; return; }
      if (e.target.closest('[data-flip]')) { session.flipped = true; hub.render(); hub.app.querySelector('[data-rate]')?.focus(); return; }
      const rate = e.target.closest('[data-rate]');
      if (rate) {
        const rating = Number(rate.dataset.rate);
        const key = session.queue.shift();
        const s = srs();
        const wasNew = !!s[key].fresh;
        s[key] = F().review(wasNew ? null : s[key], rating, now());
        setSrs(s);
        if (wasNew) {
          const today = store.get('leon-learn-srs-day', { date: '', fresh: 0 });
          store.set('leon-learn-srs-day', { date: dayStamp(), fresh: (today.date === dayStamp() ? today.fresh : 0) + 1 });
        }
        // forgotten cards come back once more in this round, without counting twice
        if (rating === F().AGAIN) { session.queue.push(key); session.total += 1; }
        session.done += 1;
        session.content = null;
        hub.render();
        hub.app.querySelector('[data-flip], .q-actions a')?.focus();
        return;
      }
      const readBtn = e.target.closest('[data-deck-read]');
      const allBtn = e.target.closest('[data-deck-all]');
      if (readBtn || allBtn) {
        const id = (readBtn || allBtn).dataset[readBtn ? 'deckRead' : 'deckAll'];
        const data = await loadCourse(id);
        const read = readCount(id);
        enqueue(data.cards.length ? data.cards.filter((c) => allBtn || read.has(c.topic)).map((c) => `${id}/${c.id}`) : data.questions.map((q) => `q:${id}/${q.id}`));
        hub.render();
      }
    });
  }

  /* ------------------------------------------------------------ labs */
  function labsView(cid) {
    if (!cid) {
      const picks = ['comp2017', 'info1113', 'comp2123', 'ml'].filter((id) => BY_ID[id]?.study.labs);
      return frame('practice', `<div class="page-head"><div><h1>${t('labsTitle')}</h1><p>${t('labsSub')}</p></div></div><div class="route-cards">${picks.map((id) => `<a class="panel route-card" href="#/labs/${id}" style="--accent:${BY_ID[id].color}"><span class="icon-tile" style="--accent:${BY_ID[id].color}">${icon(BY_ID[id].icon)}</span><span><span class="code">${esc(BY_ID[id].code)}</span><b>${esc(L(BY_ID[id].title))}</b></span></a>`).join('')}</div>`);
    }
    return withCourse(cid, 'practice', (data) => {
      const c = BY_ID[cid];
      const cards = data.labs.map((lab) => `<a class="panel route-card" href="#/lab/${cid}/${lab.id}" style="--accent:${c.color}"><span class="icon-tile" style="--accent:${c.color}">${icon('code')}</span><span><b>${esc(L(lab.title))}</b><small>${inline(L(lab.summary))}</small></span></a>`).join('');
      return frame('practice', `${crumbs([t('labsTitle'), '#/labs'], [c.code])}<div class="page-head"><div><h1>${esc(L(c.title))}</h1><p>${t('labsSub')}</p></div></div><div class="route-cards">${cards}</div>`);
    });
  }
  function labView(cid, id) {
    return withCourse(cid, 'practice', (data) => {
      const c = BY_ID[cid];
      const lab = data.labs.find((x) => x.id === id);
      if (!lab) return hub.notFound();
      const steps = lab.steps.map((s) => `<li><h4>${esc(L(s.title))}</h4>${rich(L(s.body))}${s.patch ? `<pre class="study-code"><del>${esc(s.patch.from)}</del>\n<ins>${esc(s.patch.to)}</ins></pre>` : ''}${s.command ? `<pre class="study-code">$ ${esc(s.command)}</pre>` : ''}${s.output ? `<h5>${t('labCaptured')}</h5><pre class="study-code output">${esc(s.output)}</pre>` : ''}</li>`).join('');
      return frame('practice', `${crumbs([t('labsTitle'), '#/labs'], [c.code, `#/labs/${cid}`], [L(lab.title)])}<article class="panel q-panel lab" style="--accent:${c.color}"><header><div class="tags">${(lab.tools || []).map((x) => `<span class="tag">${esc(x)}</span>`).join('')}${lab.minutes ? `<span class="tag">${esc(t('minutes')(lab.minutes))}</span>` : ''}</div><h1>${esc(L(lab.title))}</h1></header><h4>${t('labScenario')}</h4>${rich(L(lab.scenario))}${(lab.files || []).map((f) => `<h4>${esc(f.path)}</h4>${codeBlock(f.text)}`).join('')}<h4>${t('labSteps')}</h4><ol class="study-list lab-steps">${steps}</ol>${lab.review ? `<h4>${t('labReview')}</h4><ul class="study-list">${lab.review.map((x) => `<li>${inline(L(x))}</li>`).join('')}</ul>` : ''}${lab.tradeoffs ? `<h4>${t('labTrade')}</h4>${rich(L(lab.tradeoffs))}` : ''}${lab.done ? `<h4>${t('labCheck')}</h4><ul class="study-list">${lab.done.map((x) => `<li>${inline(L(x))}</li>`).join('')}</ul>` : ''}</article>`);
    });
  }

  /* ------------------------------------------------------------ backup */
  const backupKeys = () => { const keys = []; try { for (let i = 0; i < localStorage.length; i += 1) { const k = localStorage.key(i); if (/^(leon-|guoliang-|python-zero-practice)/.test(k)) keys.push(k); } } catch (_) { /* private mode */ } return keys; };
  function backupPanel() {
    return `<section class="panel study-section-panel"><div class="panel-head"><h2>${t('backupTitle')}</h2></div><div class="panel-body"><p class="muted">${t('backupSub')}</p><div class="q-actions"><button type="button" class="btn ghost sm" data-backup-export>${t('exportB')}</button><label class="btn ghost sm file-btn">${t('importB')}<input type="file" accept="application/json,.json" data-backup-import hidden></label></div><p class="muted" data-backup-note aria-live="polite"></p></div></section>`;
  }
  function wireBackup() {
    const root = hub.app.querySelector('main');
    root.querySelector('[data-backup-export]')?.addEventListener('click', () => {
      const out = {};
      backupKeys().forEach((k) => { try { out[k] = localStorage.getItem(k); } catch (_) { /* blocked: nothing to export */ } });
      const url = URL.createObjectURL(new Blob([JSON.stringify({ site: 'leon-learn', saved: new Date().toISOString(), data: out }, null, 1)], { type: 'application/json' }));
      const a = Object.assign(document.createElement('a'), { href: url, download: `leon-learn-progress-${dayStamp()}.json` });
      a.click();
      URL.revokeObjectURL(url);
    });
    root.querySelector('[data-backup-import]')?.addEventListener('change', async (e) => {
      const note = root.querySelector('[data-backup-note]');
      try {
        const parsed = JSON.parse(await e.target.files[0].text());
        if (parsed.site !== 'leon-learn' || typeof parsed.data !== 'object') throw new Error('not ours');
        Object.entries(parsed.data).forEach(([k, v]) => { if (/^(leon-|guoliang-|python-zero-practice)/.test(k) && typeof v === 'string') localStorage.setItem(k, v); });
        note.textContent = t('importedOk');
        setTimeout(() => location.reload(), 800);
      } catch (_) { note.textContent = t('importBad'); }
    });
  }

  /* ------------------------------------------------------------ router hook */
  return {
    t,
    goalBanner,
    resumeRoute,
    glancePanel,
    backupPanel,
    wireBackup,
    dueStats,
    match(parts) {
      if (parts[0] === 'start') return { page: 'start' };
      if (parts[0] === 'goal') return { page: 'goal', goal: parts[1], course: parts[2] };
      if (parts[0] === 'practice') return parts[2] ? { page: 'question', cid: parts[1], qid: parts[2] } : parts[1] ? { page: 'practiceCourse', cid: parts[1] } : { page: 'practice' };
      if (parts[0] === 'exam') return { page: 'exam', cid: parts[1], pid: parts[2] };
      if (parts[0] === 'review') return { page: parts[1] === 'run' ? 'session' : 'review' };
      if (parts[0] === 'labs') return parts[2] ? { page: 'lab', cid: parts[1], id: parts[2] } : { page: 'labs', cid: parts[1] };
      if (parts[0] === 'lab') return { page: 'lab', cid: parts[1], id: parts[2] };
      return null;
    },
    view(r) {
      if (r.page !== 'question') qs = null;
      return {
        start: startView, goal: () => goalView(r.goal, r.course), practice: practiceHome, practiceCourse: () => practiceCourse(r.cid), question: () => questionView(r.cid, r.qid),
        exam: () => examView(r.cid, r.pid), review: reviewHome, session: sessionView, labs: () => labsView(r.cid), lab: () => labView(r.cid, r.id),
      }[r.page]();
    },
    wire(r) {
      if (r.page === 'goal') {
        hub.app.querySelector('.route-steps')?.addEventListener('click', (e) => {
          const b = e.target.closest('[data-step-done]');
          if (!b) return;
          const done = routeDone(r.goal, r.course);
          setRouteDone(r.goal, r.course, { ...done, [b.dataset.stepDone]: !done[b.dataset.stepDone] });
          hub.render();
        });
      }
      if (r.page === 'question') wireQuestion(r.cid, r.qid);
      if (r.page === 'exam') wireExam(r.cid, r.pid);
      if (r.page === 'review' || r.page === 'session') wireReview();
      if (r.page === 'practiceCourse') {
        hub.app.querySelector('[data-topic-filter]')?.addEventListener('change', (e) => {
          const p = new URLSearchParams(location.hash.split('?')[1] || '');
          if (e.target.value) p.set('topic', e.target.value); else p.delete('topic');
          const s = p.toString();
          location.hash = `#/practice/${r.cid}${s ? `?${s}` : ''}`;
        });
      }
    },
    title(r) {
      const names = { start: t('startTitle'), goal: t('navStart'), practice: t('practiceTitle'), practiceCourse: t('practiceTitle'), question: t('practiceTitle'), exam: t('examsTitle'), review: t('reviewTitle'), session: t('reviewTitle'), labs: t('labsTitle'), lab: t('labsTitle') };
      return names[r.page];
    },
  };
};
