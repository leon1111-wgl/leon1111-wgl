"""阶段 3：有效记录 -> 可继续使用的统计结果。"""
from step02_collect import collect_rows, sample_rows


def ranking_key(row):
    return (-row["score"], row["student_id"])


def summarize(records):
    """前置：records 已清洗，每条 score 是 0—100 的整数。"""
    count = len(records)
    total = 0
    passed = 0
    for row in records:
        total += row["score"]
        if row["score"] >= 60:
            passed += 1
    return {
        "valid_count": count,
        "total": total,
        "mean": total / count if count else None,
        "pass_rate": passed / count if count else None,
        "ranking": sorted(records, key=ranking_key),
    }


def main():
    valid, errors = collect_rows(sample_rows())
    report = summarize(valid)
    print(f"有效 {report['valid_count']} 条，无效 {len(errors)} 条")
    print(f"总分 {report['total']}，平均分 {report['mean']:.1f}")
    print(f"通过率 {report['pass_rate']:.1%}")
    print("排名：", [row["student_id"] for row in report["ranking"]])
    empty = summarize([])
    print(f"空列表：人数 {empty['valid_count']}，平均分 {empty['mean']}，通过率 {empty['pass_rate']}")


if __name__ == "__main__":
    main()
