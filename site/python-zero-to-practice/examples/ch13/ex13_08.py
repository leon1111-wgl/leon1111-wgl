# AI 数据排错：保留坏行位置，继续处理下一行
import json

def read_training_lines(text):
    records, errors = [], []
    blank_lines = 0
    for line_number, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            blank_lines += 1
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            errors.append({"line": line_number, "kind": "json"})
            continue
        if not isinstance(item, dict):
            errors.append({"line": line_number, "kind": "schema"})
            continue
        content = item.get("text")
        label = item.get("label")
        if not isinstance(content, str) or type(label) is not int:
            errors.append({"line": line_number, "kind": "schema"})
            continue
        if not content.strip() or label not in (0, 1):
            errors.append({"line": line_number, "kind": "value"})
            continue
        records.append({"text": content.strip(), "label": label})
    return records, errors, blank_lines

text = '\n'.join([
    '{"text": " Python ", "label": 1}',
    '',
    '{"text": "broken", "label": 0',
    '{"text": 42, "label": 0}',
    '{"text": "hello", "label": 2}',
    '{"text": "Agent", "label": 0}',
])
records, errors, blank_lines = read_training_lines(text)
print(f"保留 {len(records)} 条，跳过 {blank_lines} 个空行")
for error in errors:
    print(f"第 {error['line']} 行：{error['kind']}")
print(records)
