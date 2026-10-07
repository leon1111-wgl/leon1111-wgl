# 第 12_04 题 JSONL 有效记录
# 实现 parse_jsonl(text)，跳过空行，解析其余每行 JSON，返回列表。假定非空行都是合法 JSON。打印两条 {"id":1}、{"id":2} 的结果。
# 预期程序输出：
# [{'id': 1}, {'id': 2}]

import json

def parse_jsonl(text):
    records = []
    for line in text.splitlines():
        if line.strip():
            records.append(json.loads(line))
    return records

print(parse_jsonl('{"id":1}\n\n{"id":2}\n'))
