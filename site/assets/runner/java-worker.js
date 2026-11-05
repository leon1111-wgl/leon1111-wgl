/* Java in the browser: TeaVM's build of javac compiles to WebAssembly GC in memory, then runs Main.main. */
import { load } from './java/compiler.wasm-runtime.js';

const base = new URL('./java/', import.meta.url);
let compiler = null;
let diagnostics = [];

function ready() {
  if (!compiler) {
    compiler = (async () => {
      const bytes = async (name) => {
        const res = await fetch(new URL(name, base));
        if (!res.ok) throw new Error(`${name}: ${res.status}`);
        return new Int8Array(await res.arrayBuffer());
      };
      const [teavm, sdk, runtime] = await Promise.all([load(new URL('compiler.wasm', base).href, {}), bytes('compile-classlib.bin'), bytes('runtime-classlib.bin')]);
      const c = teavm.exports.createCompiler();
      c.setSdk(sdk);
      c.setTeaVMClasslib(runtime);
      c.onDiagnostic((d) => { if (d.severity === 'error') diagnostics.push(`Main.java:${d.lineNumber}: ${d.message}`); });
      return c;
    })();
  }
  return compiler;
}

// the browser library's Formatter has no %n; a newline means the same here
const portable = (text) => text.replace(/(^|[^%])%n/g, '$1\\n');

async function compile(data) {
  const c = await ready();
  diagnostics = [];
  c.clearSourceFiles();
  c.clearOutputFiles();
  // a class written on paper may leave out its imports; practice runs supply the usual one on the first line, so line numbers stay true
  c.addSourceFile('Main.java', (data.tests && !/^\s*import\s+java\.util\.\*/m.test(data.code) ? 'import java.util.*; ' : '') + portable(data.code));
  if (data.tests) c.addSourceFile('Tests.java', portable(data.tests));
  const ok = c.compile() && c.generateWebAssembly({ outputName: 'app', mainClass: data.tests ? 'Tests' : 'Main', strictMode: true });
  return { c, ok };
}

self.onmessage = async ({ data }) => {
  try {
    if (data.kind === 'load') { await ready(); return; }
    self.postMessage({ kind: 'status', stage: 'compiling' });
    const { c, ok } = await compile(data);
    if (!ok) {
      self.postMessage({ kind: 'result', status: 'compile', stdout: '', stderr: `${diagnostics.join('\n')}\n` });
      return;
    }
    const wasm = c.getWebAssemblyOutputFile('app.wasm');
    let stdout = '';
    let stderr = '';
    const program = await load(new Uint8Array(wasm).buffer, {
      installImports(imports) {
        imports.teavmConsole.putcharStdout = (ch) => { stdout += String.fromCharCode(ch); };
        imports.teavmConsole.putcharStderr = (ch) => { stderr += String.fromCharCode(ch); };
      },
    });
    self.postMessage({ kind: 'status', stage: 'running' });
    let status = 'ok';
    try {
      await program.exports.main([]);
    } catch (error) {
      status = 'error';
      const text = String(error?.message || error);
      // two failures arrive as WebAssembly traps rather than Java exceptions, and catch blocks cannot see them
      stderr += text === 'divide by zero' ? 'java.lang.ArithmeticException: / by zero (the browser Java cannot catch this one; a real JDK can)\n'
        : text === 'illegal cast' ? 'java.lang.ArrayStoreException (the browser Java cannot catch this one; a real JDK can)\n'
          : `Uncaught exception: ${text}\n`;
    }
    // a started thread may still be printing; give it a moment
    await new Promise((resolve) => { setTimeout(resolve, 30); });
    self.postMessage({ kind: 'result', status, stdout, stderr });
  } catch (error) {
    self.postMessage({ kind: 'failed', message: String(error?.message || error) });
  }
};
