"""迁移参考：只整理固定日志，不调用模型或外部工具。"""

def clean_tool_rows(rows):
    valid = []
    errors = []
    seen = set()
    for record_number, row in enumerate(rows, start=1):
        try:
            if None in row:
                raise ValueError("字段数超过表头列数")
            task_id = (row.get("id") or "").strip()
            tool = (row.get("tool") or "").strip()
            if not task_id or not tool:
                raise ValueError("ID 或工具名为空")
            try:
                milliseconds = int(row.get("ms") or "")
            except ValueError:
                raise ValueError("耗时不是整数") from None
            if milliseconds < 0:
                raise ValueError("耗时不能为负数")
            if task_id in seen:
                raise ValueError("重复 ID")
        except ValueError as error:
            errors.append({"record": record_number, "reason": str(error)})
            continue
        seen.add(task_id)
        valid.append({"id": task_id, "tool": tool, "ms": milliseconds})
    return valid, errors


def sample_logs():
    return [
        {"id": "t1", "tool": "search", "ms": "0"},
        {"id": "t2", "tool": "fetch", "ms": "250"},
        {"id": "t3", "tool": "search", "ms": "bad"},
        {"id": "t3", "tool": "search", "ms": "30"},
        {"id": "t1", "tool": "fetch", "ms": "8"},
    ]


def main():
    valid, errors = clean_tool_rows(sample_logs())
    print("保留 ID：", [row["id"] for row in valid])
    print("耗时：", [row["ms"] for row in valid])
    print("总耗时：", sum(row["ms"] for row in valid), "毫秒")
    for error in errors:
        print(f"记录 {error['record']}：{error['reason']}")


if __name__ == "__main__":
    main()
