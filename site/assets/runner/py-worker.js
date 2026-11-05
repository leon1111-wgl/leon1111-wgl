/* Python in the browser: Pyodide, pinned, from jsDelivr. Same engine as the Python handbook's Run button. */
const PYODIDE = 'https://cdn.jsdelivr.net/pyodide/v0.27.7/full/';
let ready = null;
function boot() {
  if (!ready) {
    ready = (async () => {
      importScripts(`${PYODIDE}pyodide.js`);
      return loadPyodide({ indexURL: PYODIDE });
    })();
  }
  return ready;
}
const RUN = `
import contextlib, io, json, linecache, os, sys, tempfile, traceback
job = json.loads(job_json)
out, err = io.StringIO(), io.StringIO()

def load(name, source):
    linecache.cache[name] = (len(source), None, source.splitlines(True), name)
    return compile(source, name, 'exec')

def report(error):
    if isinstance(error, SyntaxError):
        traceback.print_exception(type(error), error, None, file=err)
    else:
        traceback.print_exception(type(error), error, error.__traceback__.tb_next, file=err)

here = os.getcwd()
os.chdir(tempfile.mkdtemp())
sys.stdin = io.StringIO(job['stdin'])
namespace = {'__name__': '__main__'}
status = 'ok'
try:
    with contextlib.redirect_stdout(out):
        try:
            exec(load('main.py', job['code']), namespace)
        except SystemExit as error:
            if error.code not in (None, 0):
                status = 'error'
                print('SystemExit(' + repr(error.code) + ')', file=err)
        except BaseException as error:
            status = 'error'
            report(error)
    if status == 'ok' and job.get('tests'):
        with contextlib.redirect_stdout(out):
            try:
                exec(load('tests', job['tests'] + '\\n'), namespace)
            except BaseException as error:
                status = 'tests'
                report(error)
finally:
    os.chdir(here)
    sys.stdin = sys.__stdin__
json.dumps({'stdout': out.getvalue()[:20000], 'stderr': err.getvalue()[-6000:], 'status': status})
`;
self.onmessage = async ({ data }) => {
  try {
    const py = await boot();
    if (data.kind === 'load') return;
    self.postMessage({ kind: 'status', stage: 'running' });
    if (/^\s*(import|from)\s+numpy/m.test(data.code)) await py.loadPackage('numpy', { messageCallback: () => {} });
    py.globals.set('job_json', JSON.stringify(data));
    self.postMessage({ kind: 'result', ...JSON.parse(py.runPython(RUN)) });
  } catch (error) {
    self.postMessage({ kind: 'failed', message: String(error?.message || error) });
  }
};
