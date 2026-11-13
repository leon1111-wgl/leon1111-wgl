#!/usr/bin/env node
/* Learner walk: four readers each try a real task on the built site, at desktop and at 375 px, in dark and in light.
     zero      never programmed, reads Chinese: pick a goal, run a first program, make a typo, come back the next day
     exam      exam in COMP2123, reads Chinese: diagnostic paper, revise a weak chapter, step through an algorithm, look things up
     paper     writes C by hand, reads English: predict, trace and write by keyboard only, then type the answer in and run it
     engineer  at work, reads English: look something up from the homepage and the hub, open the chapter on a phone, run a lab
   Each step is timed. With WALK_SHOTS=<dir> every step is saved as a screenshot; with WALK_REPORT=<file> the timings and
   checks are written as JSON. The friction points this walk found in the 2026-11 release are checks W1 to W8 below, so
   each fails if its friction comes back. Needs playwright-core and Chromium or Chrome; axe-core is used when installed. */
import { createServer } from 'node:http';
import { readFileSync, existsSync, statSync, mkdirSync, writeFileSync } from 'node:fs';
import { extname, join, resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';
import assert from 'node:assert/strict';

const require = createRequire(process.env.PLAYWRIGHT_FROM || import.meta.url);
const { chromium } = require('playwright-core');
let axeSource = null;
try { axeSource = readFileSync(createRequire(import.meta.url).resolve('axe-core/axe.min.js'), 'utf8'); } catch (_) { /* optional */ }
const SITE = join(resolve(dirname(fileURLToPath(import.meta.url)), '..'), 'site');
const SHOTS = process.env.WALK_SHOTS || '';
if (SHOTS) mkdirSync(SHOTS, { recursive: true });
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.json': 'application/json', '.css': 'text/css', '.wasm': 'application/wasm', '.svg': 'image/svg+xml', '.png': 'image/png', '.zip': 'application/zip', '.bin': 'application/octet-stream' };
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
const MATRIX = ['dark', 'light'].flatMap((theme) => [['desktop', { width: 1280, height: 900 }], ['phone', { width: 375, height: 812 }]].map(([width, viewport]) => ({ theme, width, viewport, label: `${width} ${theme}` })));
const report = { site: origin, walks: [], checks: [] };
const results = [];

/* the questions each reader typed, and the chapters that teach the answer (any of them in the first three hits is right).
   `none` lists chapters that must not come first: they only share letters with the query. */
const LOOKUPS = {
  zh: [
    ['二分查找', ['comp2123/recurrences-merge-sort', 'comp2123/bst-range-queries']],
    ['时间复杂度', ['comp2123/analysis-correctness']],
    ['最短路径', ['comp2123/dijkstra-relaxation', 'comp2123/bfs-distance']],
    ['哈希表', ['comp2123/hashing-collisions', 'info1113/equality-hashing']],
    ['梯度下降', ['ml/gradient-descent-scaling', 'start/slopes-gradients', 'comp3308/neural-training']],
    ['内存泄漏', ['info1113/memory-diagrams', 'comp2017/memory-layout', 'comp2017/allocation-ownership', 'comp2017/debugging-evidence']],
    ['段错误', ['comp2017/memory-layout', 'comp2017/pointers-arrays', 'comp2017/allocation-ownership']],
    ['竞态条件', ['comp2017/data-races-mutexes']],
    ['过拟合', ['ml/validation-regularization-shift', 'comp3308/tree-generalization', 'ml/trees-ensembles']],
    ['列表推导式', ['python/c10']],
  ],
  en: [
    ['binary search', ['comp2123/recurrences-merge-sort', 'comp2123/bst-range-queries']],
    ['big O', ['comp2123/analysis-correctness']],
    ['shortest path', ['comp2123/dijkstra-relaxation', 'comp2123/bfs-distance']],
    ['hash table', ['comp2123/hashing-collisions', 'info1113/equality-hashing']],
    ['gradient descent', ['ml/gradient-descent-scaling', 'start/slopes-gradients', 'comp3308/neural-training']],
    ['memory leak', ['info1113/memory-diagrams', 'comp2017/memory-layout', 'comp2017/allocation-ownership', 'comp2017/debugging-evidence']],
    ['segfault', ['comp2017/memory-layout', 'comp2017/pointers-arrays', 'comp2017/allocation-ownership']],
    ['race condition', ['comp2017/data-races-mutexes']],
    ['cross validation', ['comp3308/evaluation-design', 'ml/framing-splits-leakage', 'ml/validation-regularization-shift']],
    ['IoU', ['vision/detection-overlap', 'vision/detection-average-precision']],
    ['RAG', ['multimodal/multimodal-rag']],
  ],
};

const watch = (page) => {
  const errors = [];
  page.on('pageerror', (e) => errors.push(e.message));
  page.on('console', (m) => { if (m.type() === 'error' && !/favicon/.test(m.text())) errors.push(`${m.text()} [${m.location().url}]`); });
  return errors;
};

for (const { theme, width, viewport, label } of MATRIX) {
  for (const reader of ['zero', 'exam', 'paper', 'engineer']) {
    const language = reader === 'zero' || reader === 'exam' ? 'zh' : 'en';
    const context = await browser.newContext({ viewport, hasTouch: width === 'phone', reducedMotion: 'reduce' });
    const page = await context.newPage();
    const errors = watch(page);
    const walk = { reader, label, language, steps: [] };
    report.walks.push(walk);
    let shotNo = 0;
    const started = Date.now();
    const shot = async (name) => {
      walk.steps.push({ name, ms: Date.now() - started });
      if (SHOTS) await page.screenshot({ path: join(SHOTS, `${reader}-${width}-${theme}-${String(++shotNo).padStart(2, '0')}-${name}.png`) });
    };
    /* one check: a friction id from the walk (W1..W8), the readers it hurts, and what the reader must be able to do */
    const check = async (id, name, fn) => {
      const entry = { id, reader, label, name };
      try { await fn(); entry.ok = true; results.push(`ok   ${label} ${reader}: ${id} ${name}`); } catch (error) { entry.ok = false; entry.error = error.message.split('\n')[0]; results.push(`FAIL ${label} ${reader}: ${id} ${name}: ${entry.error}`); }
      report.checks.push(entry);
    };
    const settle = async () => { await page.waitForFunction(() => !document.querySelector('[data-load]')); await page.waitForTimeout(80); };
    const learn = async (hash) => { await page.goto(`${origin}/learn/${hash}`); await settle(); };
    await page.goto(`${origin}/learn/`);
    await page.evaluate(([l, th]) => { localStorage.clear(); localStorage.setItem('guoliang-language', l); localStorage.setItem('guoliang-theme', th); }, [language, theme]);
    await page.reload();

    /* the hub's search box, as typed */
    const hubSearch = async (query) => {
      await learn('#/courses');
      const box = page.locator('[data-q]');
      await box.click();
      await box.fill('');
      await box.pressSequentially(query, { delay: 5 });
      await page.waitForTimeout(350);
      return page.locator('.hit-list li a').evaluateAll((links) => links.map((a) => { const u = new URL(a.href); const parts = u.pathname.split('/'); let file = parts.pop().replace(/\.html$/, '').replace(/\.(zh|en)$/, ''); if (file === 'index') file = parts.pop(); return { file, hash: u.hash.slice(1) }; }));
    };
    const chapterOf = (hit) => `${hit.file === 'python-zero-to-practice' ? 'python' : hit.file}/${hit.hash}`;
    const lookups = async (queries) => {
      const wrong = [];
      for (const [query, right] of queries) {
        const hits = (await hubSearch(query)).slice(0, 3).map(chapterOf);
        if (!hits.some((h) => right.includes(h))) wrong.push(`"${query}" → ${hits.length ? hits.join(', ') : 'nothing'}`);
      }
      assert.equal(wrong.length, 0, `${wrong.length} of ${queries.length} lookups miss: ${wrong.join('; ')}`);
    };

    if (reader === 'zero') {
      await learn('');
      await shot('hub-intro');
      await page.click('a[href="#/start"]');
      await page.waitForSelector('.goal-card');
      await page.click('.goal-card[href="#/goal/zero"]');
      await page.waitForSelector('.route-step');
      await shot('route');
      const first = await page.locator('.route-step').first().locator('a.btn').getAttribute('href');
      await page.goto(new URL(first, `${origin}/learn/`).href);
      await page.waitForSelector('.run-button');
      const run = page.locator('.run-button').first();
      await run.scrollIntoViewIfNeeded();
      await run.click();
      await page.waitForFunction(() => document.querySelector('.run-panel[data-state="good"]'), null, { timeout: 60000 });
      await shot('first-run');
      await check('W5', 'a typo in the first program is explained in Chinese, with the line', async () => {
        const section = page.locator('.code-example[data-run="python"]').first();
        await section.locator('.code-actions button', { hasText: '修改代码' }).click();
        const editor = section.locator('.run-editor');
        await editor.fill((await editor.inputValue()).replace('print(', 'pirnt('));
        await section.locator('.run-button').click();
        await page.waitForFunction(() => document.querySelector('.code-example .run-panel[data-state="bad"]'), null, { timeout: 30000 });
        const text = await section.locator('.run-panel').innerText();
        await shot('typo-explained');
        assert.match(text, /第 \d+ 行/, 'the panel does not say which line, in Chinese');
        assert.match(text, /pirnt/, 'the panel does not name the unknown word');
        assert.match(text, /拼写|没有定义|不认识/, 'no Chinese explanation of NameError');
      });
      await learn('#/goal/zero');
      await page.locator('[data-step-done]').first().click();
      await page.waitForSelector('.route-step.done');
      await check('W1', 'next day, the hub opens with the next step of the route one click away', async () => {
        await page.goto(`${origin}/learn/`);
        await page.waitForTimeout(400);
        await shot('next-day');
        const link = page.locator('[data-resume-route]');
        assert.equal(await link.count(), 1, 'the hub intro has no link to the next route step');
        assert.match(await link.innerText(), /变量、类型和文字/, 'the resume link does not name step 2');
        await link.click();
        await page.waitForURL((u) => !u.href.endsWith('/learn/'));
      });
    }

    if (reader === 'exam') {
      await learn('#/goal/exam/comp2123');
      await page.waitForSelector('.route-step');
      await shot('route');
      await page.locator('.route-step').first().locator('a.btn').click();
      await page.waitForSelector('[data-exam-begin]');
      await page.click('[data-exam-begin]');
      await page.waitForSelector('[data-exam-clock]');
      const choices = await page.locator('input[data-exam-choice]').evaluateAll((els) => [...new Set(els.map((e) => e.dataset.examChoice))]);
      for (const q of choices) await page.locator(`input[data-exam-choice="${q}"]`).first().check();
      page.once('dialog', (d) => d.accept());
      await page.locator('[data-exam-submit]').first().click();
      await page.waitForSelector('.weak-list li');
      await shot('diagnostic-result');
      const revise = await page.locator('.weak-list li .btn').first().getAttribute('href');
      await page.goto(new URL(revise, `${origin}/learn/`).href);
      const chapter = new URL(revise, origin).hash.slice(1);
      await page.waitForSelector(`article#${chapter}`);
      await shot('weak-chapter');
      await check('W3', 'the weak chapter asks a question mid-chapter and answers at once, with a hint first', async () => {
        const box = page.locator(`article#${chapter} .quick-check`).first();
        assert.equal(await box.count(), 1, 'no in-chapter check before the end of the chapter');
        const after = await box.evaluate((el) => !!el.closest('article').querySelector('.code-example, .worked-problem, .guided') && [...el.closest('article').querySelectorAll('.code-example, .worked-problem')].some((x) => x.compareDocumentPosition(el) & Node.DOCUMENT_POSITION_FOLLOWING));
        assert.ok(after, 'the check sits after the worked material, not before it');
        await box.scrollIntoViewIfNeeded();
        const wrong = box.locator('[data-qc-option][data-qc-right="0"]').first();
        if (await wrong.count()) {
          await wrong.click();
          await page.waitForSelector(`article#${chapter} .quick-check [data-qc-feedback]:not(:empty)`);
          const feedback = await box.locator('[data-qc-feedback]').innerText();
          assert.match(feedback, /提示|再想想/, 'a wrong answer gets no hint');
          assert.equal(await box.locator('[data-qc-solution]').isVisible(), false, 'the answer shows after one wrong try');
          await box.locator('[data-qc-option][data-qc-right="1"]').click();
        } else {
          await box.locator('[data-qc-reveal]').click();
        }
        await page.waitForSelector(`article#${chapter} .quick-check[data-qc-state="done"]`);
        await shot('quick-check');
      });
      await check('W4', 'an algorithm trace can be stepped through one row at a time', async () => {
        await page.goto(`${origin}/courses/comp2123.zh.html#dijkstra-relaxation`);
        const trace = page.locator('#dijkstra-relaxation .trace-wrap').first();
        // the trace sits with the program's output, folded until the reader opens it
        await trace.evaluate((el) => { const d = el.closest('details'); if (d) d.open = true; });
        await trace.scrollIntoViewIfNeeded();
        const start = trace.locator('[data-step="start"]');
        assert.equal(await start.count(), 1, 'the trace has no step control');
        const rows = await trace.locator('tbody tr').count();
        assert.ok(rows >= 3);
        const shown = () => trace.locator('tbody tr:not(.step-hidden)').count();
        assert.equal(await shown(), rows, 'rows are hidden before the reader asks to step');
        await start.click();
        assert.equal(await shown(), 1, 'stepping does not start at the first row');
        const next = trace.locator('[data-step="next"]');
        await next.click();
        assert.equal(await shown(), 2);
        assert.equal(await trace.locator('tbody tr.step-current').count(), 1, 'no current row is marked');
        await trace.press('ArrowRight');
        assert.equal(await shown(), 3, 'the arrow key does not step');
        assert.match(await trace.locator('[data-step-status]').innerText(), new RegExp(`3\\s*/\\s*${rows}`), 'the step counter is missing');
        await shot('trace-stepper');
        await trace.locator('[data-step="all"]').click();
        assert.equal(await shown(), rows, '"show all" does not bring every row back');
      });
      await check('W2', 'a Chinese reader finds the chapter for what they type', async () => { await lookups(LOOKUPS.zh); await shot('search'); });
      await check('W7', 'my-learning shows route, review and practice at a glance', async () => {
        await learn('#/mine');
        const glance = page.locator('[data-glance]');
        assert.equal(await glance.count(), 1, 'no at-a-glance panel');
        const text = await glance.innerText();
        assert.match(text, /COMP2123/, 'the route in progress is not shown');
        assert.match(text, /复习|到期/, 'review is not shown');
        assert.match(text, /\d+\s*%|\d+\s*\/\s*\d+/, 'no numbers in the panel');
        await shot('at-a-glance');
      });
    }

    if (reader === 'paper') {
      await learn('#/goal/paper/comp2017');
      await page.waitForSelector('.route-step');
      await shot('route');
      await check('W6', 'a multiple-choice question can be answered by keyboard alone, and the result is announced', async () => {
        const data = await page.evaluate(() => fetch('data/comp2017.json').then((r) => r.json()));
        const q = data.questions.find((x) => x.kind === 'mcq');
        await learn(`#/practice/comp2017/${q.id}`);
        await page.waitForSelector('input[name="mcq"]');
        await page.locator('input[name="mcq"]').first().focus();
        await page.keyboard.press('Space');
        let guard = 0;
        while (!(await page.evaluate(() => document.activeElement?.matches('[data-check]'))) && guard++ < 12) await page.keyboard.press('Tab');
        assert.ok(guard < 12, 'Tab never reaches the Check button');
        const ring = await page.evaluate(() => { const s = getComputedStyle(document.activeElement); return s.outlineStyle !== 'none' && parseFloat(s.outlineWidth) >= 1; });
        assert.ok(ring, 'the focused Check button shows no focus ring');
        await page.keyboard.press('Enter');
        await page.waitForSelector('.q-result');
        /* announced: the mark sits in a live region, or focus moves onto it so a screen reader reads it */
        const live = await page.evaluate(() => { const r = document.querySelector('.q-result'); return !!r && (!!r.closest('[aria-live], [role="status"], [role="alert"]') || r.contains(document.activeElement) || document.activeElement === r); });
        assert.ok(live, 'the mark is not announced to a screen reader');
        await shot('keyboard-mcq');
      });
      await check('W5', 'typing the C answer in with a missing semicolon explains the compiler error and its line', async () => {
        const data = await page.evaluate(() => fetch('data/comp2017.json').then((r) => r.json()));
        const q = data.questions.find((x) => x.kind === 'write' && x.language === 'c');
        await learn(`#/practice/comp2017/${q.id}`);
        await page.waitForSelector('[data-answer]');
        await page.fill('[data-answer]', q.model_code);
        await page.click('[data-reveal]');
        await page.waitForSelector('[data-typed]');
        const broken = q.model_code.replace(/;(\s*\n)/, '$1');
        await page.fill('[data-typed]', broken);
        await page.click('[data-run-tests]');
        await page.waitForSelector('.q-result.fail, .q-run .run-explain', { timeout: 60000 });
        const text = await page.locator('[data-run-out]').innerText();
        await shot('compile-error');
        assert.match(text, /line \d+/i, 'the explanation does not give the line');
        assert.match(text, /semicolon/i, 'the missing semicolon is not explained');
      });
    }

    if (reader === 'engineer') {
      await page.goto(`${origin}/`);
      await page.click('[data-search-open]');
      await page.fill('.search-dialog input', 'race condition');
      await page.waitForTimeout(300);
      await shot('home-search');
      await check('W2', 'the homepage search sends "race condition" to the data-race chapter', async () => {
        const first = await page.locator('#search-results li a').evaluateAll((links) => links[0]?.getAttribute('href') || 'nothing');
        assert.match(first, /comp2017\.html#data-races-mutexes/, `first result is ${first}`);
      });
      await page.keyboard.press('Escape');
      await check('W2', 'an engineer finds the chapter for what they type', async () => { await lookups(LOOKUPS.en); await shot('hub-search'); });
      await check('W8', 'the heaviest chapter opens and can be read quickly', async () => {
        const cdp = await context.newCDPSession(page);
        if (width === 'phone') await cdp.send('Emulation.setCPUThrottlingRate', { rate: 4 });
        const t0 = Date.now();
        await page.goto(`${origin}/courses/comp2017.html#data-races-mutexes`, { waitUntil: 'commit' });
        await page.waitForFunction(() => { const a = document.querySelector('article#data-races-mutexes h2'); return a && a.getBoundingClientRect().height > 0 && document.querySelector('.run-button'); }, null, { timeout: 60000 });
        const ready = Date.now() - t0;
        const metrics = await page.evaluate(() => ({ nodes: document.getElementsByTagName('*').length, dcl: Math.round(performance.getEntriesByType('navigation')[0].domContentLoadedEventEnd) }));
        await cdp.send('Emulation.setCPUThrottlingRate', { rate: 1 });
        walk.heavy = { ready, ...metrics };
        await shot('heavy-chapter');
        /* the budget is what a reader notices: the chapter readable, and its Run buttons in place */
        const budget = width === 'phone' ? 3000 : 1500;
        assert.ok(ready <= budget, `readable after ${ready} ms (budget ${budget} ms${width === 'phone' ? ' at 4x CPU slowdown' : ''}; ${metrics.nodes} elements)`);
      });
      await learn('#/labs/comp2017');
      await page.locator('main .route-card').first().click();
      await page.waitForSelector('.lab-steps');
      await shot('lab');
      if (axeSource) {
        await check('W6', 'no serious or critical accessibility problems on the pages these readers used', async () => {
          const found = [];
          for (const url of ['/learn/#/start', '/learn/#/goal/exam/comp2123', '/learn/#/practice/comp2017', '/learn/#/review', '/learn/#/mine', '/courses/comp2123.zh.html#dijkstra-relaxation', '/bridges/python-first-steps.zh.html']) {
            await page.goto(`${origin}${url}`);
            await page.waitForTimeout(500);
            await page.addScriptTag({ content: axeSource });
            const v = await page.evaluate(async () => (await window.axe.run(document, { resultTypes: ['violations'] })).violations.filter((x) => ['serious', 'critical'].includes(x.impact)).map((x) => `${x.id} at ${x.nodes.slice(0, 3).map((n) => n.target.join(' ')).join(', ')}`));
            found.push(...v.map((x) => `${url}: ${x}`));
          }
          report.axe = report.axe || {};
          report.axe[label] = found;
          assert.equal(found.length, 0, found.join('; '));
        });
      }
    }
    await check('—', 'no page errors on the way', async () => assert.equal(errors.splice(0).join(' | '), ''));
    await check('—', 'no sideways scroll', async () => { const w = await page.evaluate(() => [document.documentElement.scrollWidth, innerWidth]); assert.ok(w[0] <= w[1] + 1, `page is ${w[0]}px wide at ${w[1]}px`); });
    walk.ms = Date.now() - started;
    await context.close();
  }
}
await browser.close();
server.close();
if (process.env.WALK_REPORT) writeFileSync(process.env.WALK_REPORT, JSON.stringify(report, null, 1));
console.log(results.join('\n'));
const failed = results.filter((r) => r.startsWith('FAIL'));
/* friction ranked by how many readers hit it and how often: the walk's own summary */
const byId = {};
for (const c of report.checks.filter((x) => !x.ok && x.id !== '—')) { byId[c.id] ??= { readers: new Set(), fails: 0 }; byId[c.id].readers.add(c.reader); byId[c.id].fails += 1; }
const ranked = Object.entries(byId).sort((a, b) => b[1].readers.size - a[1].readers.size || b[1].fails - a[1].fails);
if (ranked.length) console.log(`friction still found: ${ranked.map(([id, v]) => `${id} (${[...v.readers].join(', ')}; ${v.fails} failing runs)`).join(' · ')}`);
if (failed.length) process.exit(1);
console.log(`PASS: ${results.length} learner-walk checks, ${report.walks.length} walks`);
