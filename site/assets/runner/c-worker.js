/* C in the browser: xcc's self-hosted wcc compiles the program to WebAssembly in memory, then wasi-lite runs it. */
import { MemFS, runWasi } from './wasi-lite.js';

const base = new URL('./c/', import.meta.url);
const decoder = new TextDecoder();
const ENV = { INCLUDE: '/usr/include', LIB: '/usr/lib', PATH: '/usr/bin', PWD: '/home', HOME: '/home' };
let toolchain = null;

function load() {
  if (!toolchain) {
    toolchain = (async () => {
      const bytes = async (name) => {
        const res = await fetch(new URL(name, base));
        if (!res.ok) throw new Error(`${name}: ${res.status}`);
        return new Uint8Array(await res.arrayBuffer());
      };
      const [cc, crt, libc, headers] = await Promise.all([bytes('cc.wasm'), bytes('wcrt0.a'), bytes('wlibc.a'), fetch(new URL('include.json', base)).then((r) => r.json())]);
      const fs = new MemFS();
      fs.write('/usr/lib/wcrt0.a', crt);
      fs.write('/usr/lib/wlibc.a', libc);
      for (const [name, text] of Object.entries(headers)) fs.write(`/usr/include/${name}`, text);
      fs.write('/usr/bin/cc', new Uint8Array(0));
      fs.mkdirs('/home');
      fs.mkdirs('/tmp');
      return { module: await WebAssembly.compile(cc), fs };
    })();
  }
  return toolchain;
}

self.onmessage = async ({ data }) => {
  try {
    const { module, fs: base2 } = await load();
    if (data.kind === 'load') return;
    self.postMessage({ kind: 'status', stage: 'compiling' });
    const fs = new MemFS();
    fs.files = new Map(base2.files);
    fs.dirs = new Set(base2.dirs);
    // a tests block is appended to the same file so it can call the learner's functions
    fs.write('/home/main.c', data.tests ? `${data.code}\n#line 1 "tests"\n${data.tests}\n` : data.code);
    let log = '';
    const keep = (chunk) => { log += decoder.decode(chunk); };
    const compiled = runWasi(module, { args: ['/usr/bin/cc', '-o', '/home/a.out', '/home/main.c'], fs, cwd: '/home', env: ENV, onStdout: keep, onStderr: keep });
    const program = fs.read('/home/a.out');
    if (compiled !== 0 || !program || !program.length) {
      self.postMessage({ kind: 'result', status: 'compile', stdout: '', stderr: log });
      return;
    }
    const wasm = await WebAssembly.compile(program);
    self.postMessage({ kind: 'status', stage: 'running' });
    let stdout = '';
    let stderr = log;
    let exit;
    try {
      exit = runWasi(wasm, { args: ['main'], fs, cwd: '/home', env: ENV, stdin: data.stdin, onStdout: (c) => { stdout += decoder.decode(c); }, onStderr: (c) => { stderr += decoder.decode(c); } });
    } catch (error) {
      self.postMessage({ kind: 'result', status: 'error', stdout, stderr: `${stderr}${error.message}\n` });
      return;
    }
    if (exit === -2) stderr += 'Output limit reached; the program was stopped.\n';
    self.postMessage({ kind: 'result', status: exit === 0 ? 'ok' : 'error', exit, stdout, stderr });
  } catch (error) {
    self.postMessage({ kind: 'failed', message: String(error?.message || error) });
  }
};
