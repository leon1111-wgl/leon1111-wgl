#!/usr/bin/env node
/* Run every exported example through the site's own browser runner and compare its output.

     node scripts/verify_browser_runners.mjs            fail if a listed example no longer passes
     node scripts/verify_browser_runners.mjs --write    also rewrite content/browser-runnable.json from the results

   Needs playwright-core and a Chromium or Chrome. A Run button appears only for examples listed in that file. */
import { createServer } from 'node:http';
import { readFileSync, writeFileSync, existsSync, statSync, readdirSync } from 'node:fs';
import { extname, join, resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';

const require = createRequire(process.env.PLAYWRIGHT_FROM || import.meta.url);
const { chromium } = require('playwright-core');
const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const SITE = join(ROOT, 'site');
const LIST = join(ROOT, 'content', 'browser-runnable.json');
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.json': 'application/json', '.css': 'text/css', '.wasm': 'application/wasm', '.svg': 'image/svg+xml' };
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
const page = await browser.newPage();
await page.goto(`${origin}/learn/`);
const manifest = JSON.parse(readFileSync(join(SITE, 'examples', 'manifest.json'), 'utf8'));
const bridgeFile = join(SITE, 'bridges', 'examples.json');
const bridges = existsSync(bridgeFile) ? JSON.parse(readFileSync(bridgeFile, 'utf8')) : [];
const packDir = join(ROOT, 'content', 'practice');
const typed = [];
for (const name of existsSync(packDir) ? readdirSync(packDir).filter((f) => f.endsWith('.json')) : []) {
  for (const q of JSON.parse(readFileSync(join(packDir, name), 'utf8')).questions) {
    if (q.kind === 'write' || q.kind === 'bug') typed.push({ id: `${name}/${q.id}`, language: q.language, code: q.kind === 'write' ? q.model_code : q.fixed_code, tests: q.tests, expected: q.expected });
  }
}
const results = await page.evaluate(async ({ manifest, bridges }) => {
  const { run } = await import('/assets/runner/run.js');
  const out = [];
  for (const entry of [...manifest, ...bridges]) {
    const language = entry.language || 'python';
    const code = entry.code ?? await (await fetch(`/${entry.path}`)).text();
    const started = performance.now();
    const result = await run({ language, code });
    const same = result.stdout.replace(/\n$/, '') === entry.output.replace(/\n$/, '');
    out.push({ path: entry.path, language, ok: result.status === 'ok' && same, status: result.status, ms: Math.round(performance.now() - started), got: same ? '' : result.stdout.slice(0, 200), err: result.stderr.slice(0, 200) });
  }
  return out;
}, { manifest, bridges });
/* "Type it in and run it" on a paper-coding question has to work with the model answer. */
const typedFailures = await page.evaluate(async ({ typed }) => {
  const { run } = await import('/assets/runner/run.js');
  const failures = [];
  for (const q of typed) {
    const result = await run({ language: q.language, code: q.code, tests: q.tests });
    if (result.status !== 'ok' || result.stdout.replace(/\n$/, '') !== q.expected.replace(/\n$/, '')) failures.push(`${q.id}: ${result.status} ${result.stdout.slice(0, 120)} ${result.stderr.slice(0, 160)}`);
  }
  return failures;
}, { typed });
await browser.close();
server.close();
const passed = results.filter((r) => r.ok).map((r) => r.path).sort();
const by = {};
for (const r of results) { by[r.language] ??= { ok: 0, all: 0 }; by[r.language].all += 1; if (r.ok) by[r.language].ok += 1; }
console.log('browser runner:', JSON.stringify(by), `typed answers: ${typed.length - typedFailures.length}/${typed.length}`);
if (typedFailures.length) { console.error(typedFailures.join('\n')); if (!process.argv.includes('--write')) process.exit(1); }
if (process.argv.includes('--write')) {
  writeFileSync(LIST, `${JSON.stringify(passed, null, 0).replace(/","/g, '",\n"')}\n`);
  for (const r of results.filter((x) => !x.ok && x.language !== 'c')) console.log('not runnable:', r.path, r.status, r.err || r.got);
} else {
  const listed = existsSync(LIST) ? JSON.parse(readFileSync(LIST, 'utf8')) : [];
  const lost = listed.filter((p) => !passed.includes(p));
  if (lost.length) {
    for (const r of results.filter((x) => lost.includes(x.path))) console.error('FAILED:', r.path, r.status, r.err, r.got);
    process.exit(1);
  }
  console.log(`PASS: all ${listed.length} examples with a Run button print their expected output in the browser`);
}
