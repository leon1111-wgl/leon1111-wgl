"""内部辅助：在独立进程中执行受信任的本课程函数断言。"""
import contextlib
import io
import json
import linecache
from pathlib import Path
import runpy
import sys
import traceback

ROOT = Path(__file__).resolve().parents[1]
if __name__ == "__main__":
    path, exercise = sys.argv[1:]
    data = json.loads((ROOT / "tools" / "manifest.json").read_text(encoding="utf-8"))
    item = next(row for row in data["exercises"] if row["id"] == exercise)
    sys.stdin = io.StringIO(item.get("stdin", ""))
    with contextlib.redirect_stdout(io.StringIO()):
        namespace = runpy.run_path(path, run_name="__main__")
        filename = "题目 " + exercise + " 的额外测试"
        source = item["tests"] + "\n"
        # 给 traceback 提供源码，使失败时能直接看到具体 assert。
        linecache.cache[filename] = (len(source), None, source.splitlines(keepends=True), filename)
        try:
            exec(compile(source, filename, "exec"), namespace)
        except Exception:
            # traceback 使用上面的 linecache；解释器默认显示可能只留下行号。
            traceback.print_exc(file=sys.stderr)
            raise SystemExit(1)
