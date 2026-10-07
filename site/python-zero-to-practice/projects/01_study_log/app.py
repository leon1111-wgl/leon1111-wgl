"""学习记录本。先运行 python app.py --help 查看命令。"""
import argparse
import json
from datetime import date
from pathlib import Path

BASE = Path(__file__).resolve().parent

def validate_record(record):
    if not isinstance(record, dict):
        raise ValueError("记录必须是对象")
    if not isinstance(record.get("date"), str):
        raise ValueError("记录日期必须是字符串")
    date.fromisoformat(record["date"])
    minutes = record.get("minutes")
    if type(minutes) is not int or minutes < 0:
        raise ValueError("分钟必须是非负整数")
    topic = record.get("topic")
    if not isinstance(topic, str) or not topic.strip():
        raise ValueError("主题不能为空")

def load_records(path):
    if not path.exists():
        return []
    records = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(records, list):
        raise ValueError("记录文件最外层必须是列表")
    for record in records:
        validate_record(record)
    return records

def summarize(records):
    total = sum(record["minutes"] for record in records)
    count = len(records)
    return {"count": count, "total": total, "mean": total / count if count else None}

def add_record(path, minutes, topic, day):
    record = {"date": day, "minutes": minutes, "topic": topic.strip()}
    validate_record(record)
    records = load_records(path)
    records.append(record)
    path.parent.mkdir(parents=True, exist_ok=True)
    # 先写临时文件，再替换本项目自己的记录文件，降低中途写坏的机会。
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(path)
    return len(records)

def main():
    parser = argparse.ArgumentParser(description="学习打卡记录本")
    parser.add_argument("--store", type=Path, default=BASE / "outputs" / "study_log.json")
    sub = parser.add_subparsers(dest="command", required=True)
    add = sub.add_parser("add", help="添加一条记录")
    add.add_argument("minutes", type=int)
    add.add_argument("topic")
    add.add_argument("--date", default=date.today().isoformat())
    sub.add_parser("summary", help="查看汇总")
    args = parser.parse_args()
    try:
        if args.command == "add":
            count = add_record(args.store, args.minutes, args.topic, args.date)
            print(f"已保存 {count} 条记录")
        else:
            stats = summarize(load_records(args.store))
            print(f"记录数：{stats['count']}")
            print(f"总分钟：{stats['total']}")
            print("平均分钟：暂无" if stats["mean"] is None else f"平均分钟：{stats['mean']:.1f}")
    except (ValueError, OSError) as error:
        parser.exit(1, f"无法完成：{error}\n")

if __name__ == "__main__":
    main()
