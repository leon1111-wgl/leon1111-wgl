"""阶段 1：一条 CSV 字段字典 -> 一条清洗后的记录。"""

def parse_row(row):
    """仅接受 DictReader 形式的字段；不修改输入字典。"""
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
    return {"student_id": student_id, "name": name, "score": score}


def main():
    raw = {"student_id": "s1", "name": " 小林 ", "score": "60"}
    record = parse_row(raw)
    print(f"原始：name={raw['name']!r}，score={raw['score']!r}")
    print(f"清洗后：name={record['name']!r}，score={record['score']}，类型={type(record['score']).__name__}")
    for value in ["0", "abc", "101"]:
        try:
            result = parse_row({"student_id": "s2", "name": "小安", "score": value})
            print(f"{value!r} -> 保留 {result['score']}")
        except ValueError as error:
            print(f"{value!r} -> 拒绝：{error}")


if __name__ == "__main__":
    main()
