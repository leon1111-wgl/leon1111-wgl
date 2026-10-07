"""成绩清洗报告；只覆盖 --out 指定目录中的本项目输出文件。"""
import argparse
import csv
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

def analyze(path):
    valid = []
    errors = []
    seen = set()
    with path.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        required = {"student_id", "name", "score"}
        if not required.issubset(set(reader.fieldnames or [])):
            raise ValueError("缺少必需列 student_id、name、score")
        for record_number, row in enumerate(reader, start=1):
            try:
                if None in row:
                    raise ValueError("字段数超过表头列数")
                student_id = (row.get("student_id") or "").strip()
                name = (row.get("name") or "").strip()
                if not student_id or not name:
                    raise ValueError("ID 或姓名为空")
                try:
                    score = int(row.get("score") or "")
                except ValueError:
                    raise ValueError("分数不是整数") from None
                if not 0 <= score <= 100:
                    raise ValueError("分数超出 0 到 100")
                if student_id in seen:
                    raise ValueError("重复 ID")
            except ValueError as error:
                errors.append({"record": record_number, "reason": str(error)})
                continue
            seen.add(student_id)
            valid.append({"student_id": student_id, "name": name, "score": score})
    count = len(valid)
    total = sum(row["score"] for row in valid)
    passed = sum(row["score"] >= 60 for row in valid)
    return {
        "valid_count": count,
        "invalid_count": len(errors),
        "total": total,
        "mean": total / count if count else None,
        "pass_rate": passed / count if count else None,
        "ranking": sorted(valid, key=lambda row: (-row["score"], row["student_id"])),
        "errors": errors,
    }

def save_report(report, folder):
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    with (folder / "errors.csv").open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["record", "reason"])
        writer.writeheader()
        writer.writerows(report["errors"])

def main():
    parser = argparse.ArgumentParser(description="成绩表清洗与统计")
    parser.add_argument("--input", type=Path, default=BASE / "data" / "scores.csv")
    parser.add_argument("--out", type=Path, default=BASE / "outputs")
    args = parser.parse_args()
    try:
        report = analyze(args.input)
        save_report(report, args.out)
    except (OSError, ValueError, csv.Error) as error:
        parser.exit(1, f"处理失败：{error}\n")
    print(f"有效 {report['valid_count']} 条，无效 {report['invalid_count']} 条")
    if report["mean"] is None:
        print("没有有效分数，无法计算平均分与通过率")
    else:
        print(f"平均分 {report['mean']:.1f}")
        print(f"通过率 {report['pass_rate']:.1%}")

if __name__ == "__main__":
    main()
