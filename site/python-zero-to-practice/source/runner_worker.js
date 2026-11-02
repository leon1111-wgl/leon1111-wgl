// 浏览器中的 Python：在独立 Worker 里加载 Pyodide，主页面不会被死循环卡住。
// 只有学习者点击“运行”后才下载；版本固定，避免上游更新改变行为。
const PYODIDE = 'https://cdn.jsdelivr.net/pyodide/v0.27.7/full/';
let ready = null;
function boot() {
  if (!ready) {
    ready = (async () => {
      importScripts(PYODIDE + 'pyodide.js');
      return loadPyodide({ indexURL: PYODIDE });
    })();
  }
  return ready;
}

// 与 tools/check_practice.py 一致：给定输入、在空的临时文件夹里运行；有额外断言时，再在同一命名空间里检查。
const RUN = `
import contextlib, io, json, linecache, os, sys, tempfile, traceback
job = json.loads(job_json)
out, err = io.StringIO(), io.StringIO()

def load(name, source):
    linecache.cache[name] = (len(source), None, source.splitlines(True), name)
    return compile(source, name, 'exec')

def report(error):
    # 去掉运行器自己的那一层，只显示学习者代码里的位置
    traceback.print_exception(type(error), error, error.__traceback__.tb_next, file=err)

here = os.getcwd()
os.chdir(tempfile.mkdtemp())
sys.stdin = io.StringIO(job['stdin'])
namespace = {'__name__': '__main__'}
status = 'ok'
try:
    with contextlib.redirect_stdout(out):
        try:
            exec(load('你的代码.py', job['code']), namespace)
        except SystemExit as error:
            if error.code not in (None, 0):
                status = 'error'
                print('程序以 SystemExit(' + repr(error.code) + ') 结束', file=err)
        except BaseException as error:
            status = 'error'
            report(error)
    if status == 'ok' and job.get('tests'):
        with contextlib.redirect_stdout(io.StringIO()):
            try:
                exec(load('额外测试', job['tests'] + '\\n'), namespace)
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
    self.postMessage({ type: 'ready' });
    py.globals.set('job_json', JSON.stringify(data));
    self.postMessage({ type: 'result', ...JSON.parse(py.runPython(RUN)) });
  } catch (error) {
    self.postMessage({ type: 'failed', message: String(error && error.message || error) });
  }
};
