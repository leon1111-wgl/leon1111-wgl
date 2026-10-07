"""检查自己的练习。运行 python tools/check_practice.py --help。"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]

def normalize(text):
    return text.replace("\r\n", "\n").rstrip("\n")

def run_case(item, solutions=False, example=False):
    relative = item["path"] if not solutions else item["solution"]
    path = ROOT / relative
    if not path.exists():
        return False, f"文件不存在：{relative}"
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
    with tempfile.TemporaryDirectory(prefix="python-lesson-check-") as folder:
        try:
            result = subprocess.run([sys.executable, "-X", "utf8", str(path)],
                input=item.get("stdin", ""), capture_output=True, text=True,
                encoding="utf-8", errors="replace", cwd=folder, env=env, timeout=5)
        except subprocess.TimeoutExpired:
            return False, "超过 5 秒：检查是否出现无限循环，或多读了一次 input。"
        if result.returncode:
            return False, "运行报错：\n" + result.stderr[-4000:]
        if normalize(result.stdout) != normalize(item["output"]):
            return False, ("输出不同。\n预期：\n" + item["output"] + "实际：\n" + result.stdout[:4000]
                + "\n若看不出区别，请检查空格、大小写与额外的提示文字。")
        if not example and item.get("tests"):
            try:
                extra = subprocess.run([sys.executable, "-X", "utf8", str(ROOT / "tools" / "function_worker.py"), str(path), item["id"]],
                    capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=folder, env=env, timeout=5)
            except subprocess.TimeoutExpired:
                return False, "额外函数测试超时。请检查空输入和循环终止条件。"
            if extra.returncode:
                return False, "额外函数测试未通过：\n" + extra.stderr[-4000:]
    return True, "示例输出及额外测试通过" if item.get("tests") else "示例输出通过"

def main():
    parser = argparse.ArgumentParser(description="Python 教材练习自检；先保存文件再运行。")
    parser.add_argument("exercise", nargs="?", help="题号，例如 09_02")
    parser.add_argument("--chapter", help="章号，例如 09")
    parser.add_argument("--all", action="store_true", help="检查所有练习，未作答的会显示失败")
    parser.add_argument("--solutions", action="store_true", help="仅核验参考答案，不代表自己作答通过")
    args = parser.parse_args()
    items = json.loads((ROOT / "tools" / "manifest.json").read_text(encoding="utf-8"))["exercises"]
    if args.exercise:
        items = [item for item in items if item["id"] == args.exercise]
    elif args.chapter:
        chapter = args.chapter.zfill(2)
        items = [item for item in items if item["id"].startswith(chapter + "_")]
    elif not args.all:
        parser.error("请提供题号、--chapter 或 --all。例如：09_02")
    if not items:
        parser.error("没有找到对应题目，请检查编号。")
    failures = 0
    for item in items:
        ok, message = run_case(item, solutions=args.solutions)
        print(f"{'通过' if ok else '未通过'} {item['id']} {item['title']}")
        if not ok:
            failures += 1
            print(message)
    print(f"结果：{len(items)-failures}/{len(items)} 通过。" + ("本次检查的是参考答案。" if args.solutions else ""))
    return int(failures > 0)

if __name__ == "__main__":
    raise SystemExit(main())
