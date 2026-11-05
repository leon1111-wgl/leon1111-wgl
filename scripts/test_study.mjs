#!/usr/bin/env node
/* End-to-end checks of the learning features at desktop width and at 375 px. Needs playwright-core and Chromium or Chrome. */
import { createServer } from 'node:http';
import { readFileSync, existsSync, statSync } from 'node:fs';
import { extname, join, resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';
import assert from 'node:assert/strict';

const require = createRequire(process.env.PLAYWRIGHT_FROM || import.meta.url);
const { chromium } = require('playwright-core');
const SITE = join(resolve(dirname(fileURLToPath(import.meta.url)), '..'), 'site');
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.css': 'text/css', '.wasm': 'application/wasm', '.svg': 'image/svg+xml', '.png': 'image/png' };
const server = createServer((req, res) => {
  const path = join(SITE, decodeURIComponent(new URL(req.url, 'http://x').pathname));
  const file = existsSync(path) && statSync(path).isDirectory() ? join(path, 'index.html') : path;
  if (!file.startsWith(SITE) || !existsSync(file)) { res.writeHead(404); res.end(); return; }
  res.writeHead(200, { 'content-type': MIME[extname(file)] || 'application/octet-stream' });
  res.end(readFileSync(file));
});
await new Promise((ok) => { server.listen(0, '127.0.0.1', ok); });
const origin = `http://127.0.0.1:${server.address().port}`;
const browser = await chromium.launch({ channel: process.env.CHROME_CHANNEL || undefined, headless: true });
const results = [];
const check = async (name, fn) => { try { await fn(); results.push(`ok   ${name}`); } catch (error) { results.push(`FAIL ${name}: ${error.message.split('\n')[0]}`); } };

for (const [label, viewport] of [['desktop', { width: 1280, height: 900 }], ['phone', { width: 375, height: 812 }]]) {
  const context = await browser.newContext({ viewport, hasTouch: label === 'phone' });
  const page = await context.newPage();
  const errors = [];
  page.on('pageerror', (e) => errors.push(e.message));
  const noOverflow = async () => { const w = await page.evaluate(() => [document.documentElement.scrollWidth, innerWidth]); assert.ok(w[0] <= w[1] + 1, `page is ${w[0]}px wide at ${w[1]}px`); };
  const go = async (hash) => { await page.goto(`${origin}/learn/${hash}`); await page.waitForTimeout(150); };
  await page.goto(`${origin}/learn/#/start`);
  await page.evaluate(() => { localStorage.clear(); localStorage.setItem('guoliang-language', 'en'); });

  await check(`${label}: goal picker offers four goals and a route for each`, async () => {
    await go('#/start');
    assert.equal(await page.locator('.goal-card').count(), 4);
    await noOverflow();
    for (const [goal, course, min] of [['zero', '', 7], ['exam', 'comp2017', 7], ['exam', 'comp2022', 7], ['exam', 'comp3308', 7], ['exam', 'info1113', 7], ['exam', 'comp2123', 7], ['exam', 'python', 7], ['paper', 'comp2017', 6], ['paper', 'info1113', 6], ['paper', 'python', 5], ['paper', 'comp2123', 5], ['engineer', 'comp2017', 3], ['engineer', 'info1113', 3], ['engineer', 'comp2123', 2], ['engineer', 'ml', 2]]) {
      await go(`#/goal/${goal}${course ? `/${course}` : ''}`);
      await page.waitForSelector('.route-step');
      assert.ok(await page.locator('.route-step').count() >= min, `${goal} has too few steps`);
      await noOverflow();
    }
  });
  await check(`${label}: every route step leads to a page that exists`, async () => {
    for (const route of ['zero', 'exam/comp2022', 'paper/comp2017', 'paper/info1113', 'paper/python', 'engineer/comp2017', 'engineer/info1113', 'engineer/ml']) {
      await go(`#/goal/${route}`);
      await page.waitForSelector('.route-step');
      const links = await page.locator('.route-step .btn.primary, .route-step a.btn').evaluateAll((els) => els.map((a) => a.getAttribute('href')));
      for (const href of links.filter(Boolean)) {
        if (href.startsWith('#')) {
          await page.evaluate((h) => { location.hash = h; }, href);
          await page.waitForFunction(() => !document.querySelector('[data-load]'));
          await page.waitForTimeout(60);
          const text = await page.locator('main').textContent();
          assert.ok(!/does not exist|No questions match|没有找到这个页面/.test(text), `${route} step ${href} is a dead end`);
        } else {
          const status = await page.evaluate((u) => fetch(u.split('#')[0]).then((r) => r.status), href);
          assert.equal(status, 200, `${route} step ${href}`);
        }
      }
    }
  });
  await check(`${label}: a lab shows captured output`, async () => {
    await go('#/labs/comp2017');
    await page.waitForSelector('.route-card');
    await page.locator('main .route-card').first().click();
    await page.waitForSelector('.lab-steps');
    await noOverflow();
  });
  await check(`${label}: a first-steps guide runs its first example`, async () => {
    await page.goto(`${origin}/bridges/java-first-steps.html`);
    await page.waitForSelector('.bridge-lesson .run-button');
    await noOverflow();
    const run = page.locator('.bridge-lesson .run-button').first();
    await run.scrollIntoViewIfNeeded();
    await run.click();
    await page.waitForFunction(() => document.querySelector('.bridge-lesson .run-panel[data-state="good"]'), null, { timeout: 30000 });
  });
  await check(`${label}: tapping a defined word shows its meaning`, async () => {
    await page.goto(`${origin}/courses/comp2123.html#analysis-correctness`);
    await page.waitForSelector('article#analysis-correctness .term');
    await page.locator('article#analysis-correctness .term').first().click();
    await page.waitForSelector('.term-pop:not([hidden])');
    assert.ok((await page.textContent('.term-pop')).length > 5);
    await noOverflow();
  });
  await check(`${label}: my progress can be exported and imported`, async () => {
    await go('#/mine');
    const [download] = await Promise.all([page.waitForEvent('download'), page.click('[data-backup-export]')]);
    const path = await download.path();
    const saved = JSON.parse(readFileSync(path, 'utf8'));
    assert.equal(saved.site, 'leon-learn');
    await page.setInputFiles('[data-backup-import]', path);
    await page.waitForFunction(() => /Imported|已导入/.test(document.querySelector('[data-backup-note]')?.textContent || ''));
    await page.waitForTimeout(1000);
  });
  await check(`${label}: a finished route step stays finished after reload`, async () => {
    await go('#/goal/exam/comp2017');
    await page.waitForSelector('[data-step-done]');
    await page.locator('[data-step-done]').first().click();
    await page.waitForSelector('.route-step.done');
    await page.reload();
    await page.waitForSelector('.route-step.done');
  });
  await check(`${label}: predict-the-output marks by line and queues a wrong answer`, async () => {
    await go('#/practice/comp2017/p-pointers-arrays-c-warmup-copy-and-alias');
    await page.waitForSelector('[data-answer]');
    await page.fill('[data-answer]', 'inside copy=9\nwrong\n');
    await page.click('[data-check]');
    await page.waitForSelector('.diff');
    assert.match(await page.textContent('.q-result'), /1 \/ 3/);
    const srs = await page.evaluate(() => JSON.parse(localStorage.getItem('leon-learn-srs')));
    assert.ok('q:comp2017/p-pointers-arrays-c-warmup-copy-and-alias' in srs);
    await noOverflow();
  });
  await check(`${label}: review queue schedules with FSRS and leaves nothing due`, async () => {
    await go('#/review');
    await page.waitForSelector('[data-review-start]');
    await page.click('[data-review-start]');
    await page.waitForSelector('[data-flip]');
    await page.click('[data-flip]');
    await page.waitForSelector('[data-rate]');
    assert.equal(await page.locator('[data-rate]').count(), 4);
    await noOverflow();
    await page.click('[data-rate="3"]');
    await page.waitForFunction(() => !document.querySelector('[data-load]'));
    const state = await page.evaluate(() => Object.values(JSON.parse(localStorage.getItem('leon-learn-srs')))[0]);
    assert.ok(state.s > 0 && state.due > Date.now());
  });
  await check(`${label}: hub search finds a chapter by what it teaches`, async () => {
    await go('#/courses');
    await page.fill('[data-q]', 'malloc');
    await page.waitForFunction(() => document.querySelector('.hit-list li'));
  });
  await check(`${label}: reading page folds answers and can run C`, async () => {
    await page.goto(`${origin}/courses/comp2017.html#pointers-arrays`);
    await page.waitForSelector('article#pointers-arrays .run-button');
    assert.equal(await page.evaluate(() => document.querySelector('article#pointers-arrays details.try-first').open), false);
    const run = page.locator('article#pointers-arrays .run-button').first();
    await run.scrollIntoViewIfNeeded();
    await run.click();
    await page.waitForFunction(() => document.querySelector('article#pointers-arrays .run-panel[data-state="good"]'), null, { timeout: 15000 });
    await noOverflow();
  });
  await check(`${label}: reading page can run Java`, async () => {
    await page.goto(`${origin}/courses/info1113.html#java-execution-types`);
    await page.waitForSelector('article#java-execution-types .run-button');
    const run = page.locator('article#java-execution-types .run-button').first();
    await run.scrollIntoViewIfNeeded();
    await run.click();
    await page.waitForFunction(() => document.querySelector('article#java-execution-types .run-panel[data-state="good"]'), null, { timeout: 30000 });
  });
  if (label === 'phone') {
    await check('phone: one chapter at a time', async () => {
      await page.goto(`${origin}/courses/comp2017.html#pointers-arrays`);
      await page.waitForSelector('.phone-bar');
      const visible = await page.evaluate(() => [...document.querySelectorAll('article.topic')].filter((a) => a.offsetParent !== null).map((a) => a.id));
      assert.deepEqual(visible, ['pointers-arrays']);
      await page.click('.pb-next');
      await page.waitForFunction(() => document.querySelector('article#strings-parsing.is-open'));
      await noOverflow();
    });
  }
  await check(`${label}: homepage search opens and finds a chapter`, async () => {
    await page.goto(`${origin}/`);
    await page.click('[data-search-open]');
    await page.fill('.search-dialog input', 'malloc');
    await page.waitForSelector('#search-results li');
    await page.keyboard.press('Escape');
    assert.equal(await page.evaluate(() => document.querySelector('.search-dialog').open), false);
    await noOverflow();
  });
  await check(`${label}: hub intro fits, in both languages and both themes`, async () => {
    for (const language of ['zh', 'en']) for (const theme of ['dark', 'light']) {
      await page.goto(`${origin}/learn/`);
      await page.evaluate(([l, th]) => { localStorage.setItem('guoliang-language', l); localStorage.setItem('guoliang-theme', th); }, [language, theme]);
      await page.goto(`${origin}/learn/`);
      await page.reload();
      await page.waitForTimeout(900);
      await noOverflow();
      const hero = await page.evaluate(() => ({ opacity: Number(getComputedStyle(document.querySelector('.hero h1')).opacity), right: Math.max(...[...document.querySelectorAll('.intro-bar *')].map((x) => x.getBoundingClientRect().right)), width: innerWidth, toggle: document.querySelector('.intro-bar .segmented')?.getBoundingClientRect().height }));
      assert.ok(hero.opacity > 0.9, `hero opacity ${hero.opacity} after 900ms`);
      assert.ok(hero.right <= hero.width, `top bar reaches ${hero.right} at ${hero.width}`);
      assert.ok(hero.toggle <= 40, `language toggle wraps (${hero.toggle}px)`);
    }
    await page.evaluate(() => { localStorage.setItem('guoliang-language', 'en'); localStorage.removeItem('guoliang-theme'); });
  });
  await check(`${label}: a course file that fails to load says so and can be retried`, async () => {
    await page.route('**/learn/data/dl.json', (route) => route.abort());
    await go('#/practice/dl');
    await page.waitForSelector('[data-load] button');
    await page.unroute('**/learn/data/dl.json');
    await page.click('[data-load] button');
    await page.waitForSelector('.q-list');
  });
  await check(`${label}: a card whose question disappeared does not break the queue`, async () => {
    await page.evaluate(() => { const s = JSON.parse(localStorage.getItem('leon-learn-srs') || '{}'); s['comp2017/c-gone-check'] = { fresh: true, added: 1 }; localStorage.setItem('leon-learn-srs', JSON.stringify(s)); });
    await go('#/review/run');
    await page.waitForFunction(() => !document.querySelector('[data-load]') && document.querySelector('main').textContent.length > 20);
    const s = await page.evaluate(() => JSON.parse(localStorage.getItem('leon-learn-srs')));
    assert.ok(!('comp2017/c-gone-check' in s));
  });
  await check(`${label}: no script errors`, async () => assert.equal(errors.join(' | '), ''));
  await context.close();
}
/* every kind of question and a whole mock paper, answered with the right answers, as a reader would */
for (const [label, viewport] of [['desktop', { width: 1280, height: 900 }], ['phone', { width: 375, height: 812 }]]) {
  const context = await browser.newContext({ viewport });
  const page = await context.newPage();
  const errors = [];
  page.on('pageerror', (e) => errors.push(e.message));
  await page.goto(`${origin}/learn/#/start`);
  await page.evaluate(() => { localStorage.clear(); localStorage.setItem('guoliang-language', 'en'); });
  const data = await page.evaluate(() => fetch('data/python.json').then((r) => r.json()));
  const first = (kind) => data.questions.find((q) => q.kind === kind);
  const open = async (q) => { await page.goto(`${origin}/learn/#/practice/python/${q.id}`); await page.reload(); await page.waitForSelector('[data-q-body]'); };
  const stored = (q) => page.evaluate((id) => JSON.parse(localStorage.getItem('leon-learn-attempts'))[`python/${id}`], q.id);
  const noOverflow = async () => { const w = await page.evaluate(() => [document.documentElement.scrollWidth, innerWidth]); assert.ok(w[0] <= w[1] + 1, `page is ${w[0]}px wide at ${w[1]}px`); };
  await check(`${label}: multiple choice marks the right answer in full`, async () => {
    const q = first('mcq');
    await open(q);
    await page.locator(`input[name="mcq"][value="${q.options.findIndex((o) => o.correct)}"]`).check();
    await page.click('[data-check]');
    assert.equal((await stored(q)).score, q.marks);
    await noOverflow();
  });
  await check(`${label}: a trace table marks its blanks`, async () => {
    const q = first('trace');
    await open(q);
    for (const input of await page.locator('[data-cell]').all()) {
      const [r, c] = (await input.getAttribute('data-cell')).split(',').map(Number);
      await input.fill(q.rows[r][c]);
    }
    await page.click('[data-check]');
    assert.equal((await stored(q)).score, q.marks);
    await noOverflow();
  });
  await check(`${label}: paper coding hides the answer, marks by rubric, then runs the tests`, async () => {
    const q = first('write');
    await open(q);
    assert.ok(!(await page.locator('main').textContent()).includes(q.model_code.trim().split('\n')[0]), 'model answer visible before attempting');
    await page.fill('[data-answer]', q.model_code);
    await page.click('[data-reveal]');
    for (const box of await page.locator('[data-rubric]').all()) await box.check();
    assert.equal((await stored(q)).score, q.marks);
    await page.click('[data-run-tests]');
    await page.waitForSelector('.q-result.pass', { timeout: 120000 });
    await noOverflow();
  });
  await check(`${label}: a mock paper survives a refresh, then marks itself`, async () => {
    const paper = data.papers.find((p) => p.type === 'diagnostic');
    await page.goto(`${origin}/learn/#/exam/python/${paper.id}`);
    await page.reload();
    await page.waitForSelector('[data-exam-begin]');
    await page.click('[data-exam-begin]');
    await page.waitForSelector('[data-exam-clock]');
    const qs = paper.questions.map((id) => data.questions.find((x) => x.id === id));
    for (const q of qs) {
      if (q.kind === 'mcq') await page.locator(`input[data-exam-choice="${q.id}"][value="${q.options.findIndex((o) => o.correct)}"]`).check();
      if (q.kind === 'predict') await page.fill(`[data-exam-text="${q.id}"]`, q.output);
      if (q.kind === 'numeric') await page.fill(`[data-exam-text="${q.id}"]`, String(q.answer));
      if (q.kind === 'trace') for (const input of await page.locator(`[data-exam-cell="${q.id}"]`).all()) { const [r, c] = (await input.getAttribute('data-rc')).split(',').map(Number); await input.fill(q.rows[r][c]); }
    }
    await noOverflow();
    await page.reload();
    await page.waitForSelector('[data-exam-clock]');
    const auto = qs.find((q) => q.kind === 'mcq');
    assert.ok(await page.locator(`input[data-exam-choice="${auto.id}"][value="${auto.options.findIndex((o) => o.correct)}"]`).isChecked(), 'answer lost on refresh');
    page.once('dialog', (d) => d.accept());
    await page.locator('[data-exam-submit]').first().click();
    await page.waitForSelector('[data-exam-total]');
    const total = await page.textContent('[data-exam-total]');
    const expected = qs.filter((q) => ['mcq', 'predict', 'numeric', 'trace'].includes(q.kind)).reduce((n, q) => n + q.marks, 0);
    assert.ok(total.startsWith(`${expected} /`), `expected ${expected} marks, page says ${total}`);
    await noOverflow();
  });
  await check(`${label}: no script errors while practising`, async () => assert.equal(errors.join(' | '), ''));
  await context.close();
}

/* the homepage's own links, including the seven project cards and the learning hub */
{
  const context = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const page = await context.newPage();
  await check('homepage: project order, and every local link resolves', async () => {
    await page.goto(`${origin}/`);
    const names = await page.locator('.proj-card h3').allTextContents();
    assert.deepEqual(names, ['LoopDesk', 'ProofBI', 'AdProof', 'CreditLens', 'EstateGuard', 'FinScope', 'Career Atlas']);
    const hrefs = await page.locator('main a[href], header a[href]').evaluateAll((els) => [...new Set(els.map((a) => new URL(a.getAttribute('href'), location.href).href))]);
    for (const href of hrefs.filter((h) => h.startsWith(origin))) {
      const status = await page.evaluate((u) => fetch(u.split('#')[0]).then((r) => r.status), href);
      assert.equal(status, 200, href);
    }
  });
  await context.close();
}

/* blocked storage: everything must still work for the length of the visit */
{
  const context = await browser.newContext({ viewport: { width: 375, height: 812 } });
  await context.addInitScript(() => { Object.defineProperty(window, 'localStorage', { get() { throw new Error('blocked'); } }); Object.defineProperty(window, 'sessionStorage', { get() { throw new Error('blocked'); } }); });
  const page = await context.newPage();
  const errors = [];
  page.on('pageerror', (e) => errors.push(e.message));
  await check('blocked storage: practice and review work in memory', async () => {
    await page.goto(`${origin}/learn/#/practice/comp2017/p-pointers-arrays-c-warmup-copy-and-alias`);
    await page.waitForSelector('[data-answer]');
    await page.fill('[data-answer]', 'wrong');
    await page.click('[data-check]');
    await page.waitForSelector('.diff');
    await page.evaluate(() => { location.hash = '#/review'; });
    await page.waitForSelector('[data-review-start]');
    await page.goto(`${origin}/courses/comp2017.html#pointers-arrays`);
    await page.waitForSelector('article#pointers-arrays .run-button');
    await page.goto(`${origin}/`);
    await page.waitForSelector('[data-search-open]');
    assert.equal(errors.join(' | '), '');
  });
  await context.close();
}
await browser.close();
server.close();
console.log(results.join('\n'));
if (results.some((r) => r.startsWith('FAIL'))) process.exit(1);
console.log(`PASS: ${results.length} learning-feature checks`);
