#!/usr/bin/env node
/* Run every exported example through the site's own browser runner and compare its output.

     node scripts/verify_browser_runners.mjs            fail if a listed example no longer passes
     node scripts/verify_browser_runners.mjs --write    also rewrite content/browser-runnable.json from the results

   Needs playwright-core and a Chromium or Chrome. A Run button appears only for examples listed in that file. */
import { createServer } from 'node:http';
import { readFileSync, writeFileSync, existsSync, statSync } from 'node:fs';
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
const results = await page.evaluate(async ({ manifest }) => {
  const { run } = await import('/assets/runner/run.js');
  const out = [];
  for (const entry of manifest) {
    const language = entry.language || 'python';
    const code = await (await fetch(`/${entry.path}`)).text();
    const started = performance.now();
    const result = await run({ language, code, timeoutMs: 20000 });
    const same = result.stdout.replace(/\n$/, '') === entry.output.replace(/\n$/, '');
    out.push({ path: entry.path, language, ok: result.status === 'ok' && same, status: result.status, ms: Math.round(performance.now() - started), got: same ? '' : result.stdout.slice(0, 200), err: result.stderr.slice(0, 200) });
  }
  return out;
}, { manifest });
await browser.close();
server.close();
const passed = results.filter((r) => r.ok).map((r) => r.path).sort();
const by = {};
for (const r of results) { by[r.language] ??= { ok: 0, all: 0 }; by[r.language].all += 1; if (r.ok) by[r.language].ok += 1; }
console.log('browser runner:', JSON.stringify(by));
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
