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
    for (const [goal, course, min] of [['zero', '', 4], ['exam', 'comp2017', 2], ['paper', 'comp2017', 1], ['engineer', 'comp2017', 1], ['paper', 'info1113', 1], ['paper', 'comp2123', 1]]) {
      await go(`#/goal/${goal}${course ? `/${course}` : ''}`);
      await page.waitForSelector('.route-step');
      assert.ok(await page.locator('.route-step').count() >= min, `${goal} has too few steps`);
      await noOverflow();
    }
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
  await check(`${label}: no script errors`, async () => assert.deepEqual(errors, []));
  await context.close();
}
await browser.close();
server.close();
console.log(results.join('\n'));
if (results.some((r) => r.startsWith('FAIL'))) process.exit(1);
console.log(`PASS: ${results.length} learning-feature checks`);
