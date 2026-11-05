"""阶段 2：内存中的原始记录 -> 有效记录和错误列表。"""
from step01_parse import parse_row


def collect_rows(rows):
    valid = []
    errors = []
    seen = set()
    for record_number, row in enumerate(rows, start=1):
        try:
            record = parse_row(row)
            if record["student_id"] in seen:
                raise ValueError("重复 ID")
        except ValueError as error:
            errors.append({"record": record_number, "reason": str(error)})
            continue
        seen.add(record["student_id"])
        valid.append(record)
    return valid, errors


def sample_rows():
    return [
        {"student_id": "s1", "name": " 小林 ", "score": "60"},
        {"student_id": "s2", "name": "小安", "score": "abc"},
        {"student_id": "s2", "name": "小安", "score": "0"},
        {"student_id": "s1", "name": "小林", "score": "90"},
        {"student_id": "s3", "name": "小周", "score": "90"},
    ]


def main():
    valid, errors = collect_rows(sample_rows())
    print("有效学号：", [row["student_id"] for row in valid])
    print("有效分数：", [row["score"] for row in valid])
    for error in errors:
        print(f"记录 {error['record']}：{error['reason']}")


if __name__ == "__main__":
    main()
