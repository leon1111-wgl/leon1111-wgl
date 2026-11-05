/* Run a learner's program in this browser: Python (Pyodide), C (xcc's wcc) and Java (TeaVM's javac).
   Each language has its own worker, loaded on the first click, so a stuck loop can never freeze the page.
   The code and its output stay in this browser. */
const here = new URL('./', import.meta.url);
const SOURCES = { python: 'py-worker.js', c: 'c-worker.js', java: 'java-worker.js' };
const workers = new Map();

function workerFor(language) {
  let worker = workers.get(language);
  if (!worker) {
    worker = new Worker(new URL(SOURCES[language], here), language === 'python' ? {} : { type: 'module' });
    workers.set(language, worker);
  }
  return worker;
}

export function preload(language) {
  workerFor(language).postMessage({ kind: 'load' });
}

/* status: ok | error (runtime failure or non-zero exit) | compile | tests | timeout | unavailable
   timeoutMs counts from the moment the runtime is ready, so a slow first download is not called a hang. */
export async function run(job) {
  const first = await attempt(job);
  // Older engines can trap every few compilations in a reused Java compiler. A fresh worker recovers.
  return first.status === 'unavailable' && job.language === 'java' ? attempt(job) : first;
}

function attempt({ language, code, stdin = '', tests = '', timeoutMs = 8000, bootMs = 180000, onStatus }) {
  return new Promise((resolve) => {
    const worker = workerFor(language);
    let timer;
    const finish = (result) => {
      clearTimeout(timer);
      worker.onmessage = null;
      worker.onerror = null;
      resolve(result);
    };
    const kill = (result) => {
      worker.terminate();
      workers.delete(language);
      finish(result);
    };
    const arm = (ms, status) => {
      clearTimeout(timer);
      timer = setTimeout(() => kill({ status, stdout: '', stderr: '' }), ms);
    };
    worker.onerror = (event) => kill({ status: 'unavailable', stdout: '', stderr: String(event.message || 'worker failed') });
    worker.onmessage = ({ data }) => {
      if (data.kind === 'status') {
        onStatus?.(data.stage);
        if (data.stage === 'running') arm(timeoutMs, 'timeout');
      } else if (data.kind === 'result') {
        finish(data);
      } else if (data.kind === 'failed') {
        kill({ status: 'unavailable', stdout: '', stderr: data.message });
      }
    };
    arm(bootMs, 'unavailable');
    worker.postMessage({ kind: 'run', code, stdin, tests, language });
  });
}

export function supported(language) {
  if (typeof WebAssembly !== 'object' || typeof Worker === 'undefined') return false;
  if (language !== 'java') return true;
  // TeaVM's output needs WebAssembly GC (Chrome 119, Firefox 120, Safari 18.2): a module with one struct type
  try { return WebAssembly.validate(new Uint8Array([0, 97, 115, 109, 1, 0, 0, 0, 1, 7, 1, 95, 1, 126, 0, 95])) || WebAssembly.validate(new Uint8Array([0, 97, 115, 109, 1, 0, 0, 0, 1, 5, 1, 95, 1, 127, 0])); } catch (_) { return false; }
}
