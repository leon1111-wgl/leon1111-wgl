"""内部辅助：在独立进程中执行受信任的本课程函数断言。"""
import contextlib
import io
import json
from pathlib import Path
import runpy
import sys

ROOT = Path(__file__).resolve().parents[1]
if __name__ == "__main__":
    path, exercise = sys.argv[1:]
    data = json.loads((ROOT / "tools" / "manifest.json").read_text(encoding="utf-8"))
    item = next(row for row in data["exercises"] if row["id"] == exercise)
    sys.stdin = io.StringIO(item.get("stdin", ""))
    with contextlib.redirect_stdout(io.StringIO()):
        namespace = runpy.run_path(path, run_name="__main__")
        exec(compile(item["tests"], "题目 " + exercise + " 的额外测试", "exec"), namespace)
