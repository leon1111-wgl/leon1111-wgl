"""阶段 4：读取项目 CSV，复用前三层，只把报告打印到终端。"""
import csv
from pathlib import Path
from step02_collect import collect_rows
from step03_summary import summarize


def read_valid_rows(path):
    with path.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        required = {"student_id", "name", "score"}
        if not required.issubset(set(reader.fieldnames or [])):
            raise ValueError("缺少必需列 student_id、name、score")
        return collect_rows(reader)


def analyze(path):
    valid, errors = read_valid_rows(path)
    report = summarize(valid)
    report["invalid_count"] = len(errors)
    report["errors"] = errors
    return report


def main():
    source = Path(__file__).resolve().parent.parent / "data" / "scores.csv"
    report = analyze(source)
    print(f"有效 {report['valid_count']} 条，无效 {report['invalid_count']} 条")
    print(f"总分 {report['total']}")
    if report["mean"] is None:
        print("没有有效分数，无法计算平均分与通过率")
    else:
        print(f"平均分 {report['mean']:.1f}")
        print(f"通过率 {report['pass_rate']:.1%}")
    print("错误记录号：", [error["record"] for error in report["errors"]])


if __name__ == "__main__":
    main()
