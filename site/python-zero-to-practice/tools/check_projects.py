"""验证参考项目的数据结果、边界行为与输出文件。"""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]

def worker(folder):
    project_dir = ROOT / "projects" / folder
    spec = importlib.util.spec_from_file_location("lesson_project", project_dir / "app.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    cases = json.loads((ROOT / "tools" / "project_checks.json").read_text(encoding="utf-8"))
    checks = next(item["checks"] for item in cases if item["folder"] == folder)
    with tempfile.TemporaryDirectory(prefix="python-project-check-") as td:
        namespace = {"module": module, "temp": Path(td), "project_dir": project_dir, "json": json}
        exec(compile(checks, folder + " 验收检查", "exec"), namespace)

def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--worker":
        worker(sys.argv[2])
        return 0
    cases = json.loads((ROOT / "tools" / "project_checks.json").read_text(encoding="utf-8"))
    failures = 0
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
    for case in cases:
        try:
            result = subprocess.run([sys.executable, "-X", "utf8", str(Path(__file__).resolve()), "--worker", case["folder"]],
                capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=10, env=env)
            ok = result.returncode == 0
            print(f"{'通过' if ok else '未通过'} {case['folder']}")
            if not ok:
                failures += 1
                print(result.stderr[-4000:])
        except subprocess.TimeoutExpired:
            failures += 1
            print("未通过", case["folder"], "执行超时")
    print(f"参考项目验收：{len(cases)-failures}/{len(cases)} 通过。")
    return int(failures > 0)

if __name__ == "__main__":
    raise SystemExit(main())
