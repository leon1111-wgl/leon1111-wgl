"""运行全部示例，比较教材预期输出。仅使用标准库。"""
import json
from pathlib import Path
from check_practice import run_case

ROOT = Path(__file__).resolve().parents[1]

def main():
    items = json.loads((ROOT / "tools" / "manifest.json").read_text(encoding="utf-8"))["examples"]
    failed = []
    for item in items:
        ok, message = run_case(item, example=True)
        if not ok:
            failed.append(item["id"])
            print(item["id"], message)
    print(f"示例核验：{len(items)-len(failed)}/{len(items)} 通过。")
    return int(bool(failed))

if __name__ == "__main__":
    raise SystemExit(main())
