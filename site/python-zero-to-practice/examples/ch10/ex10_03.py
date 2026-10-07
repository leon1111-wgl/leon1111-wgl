# 按记录字段排序
records = [
    {"name": "B", "score": 90},
    {"name": "A", "score": 90},
    {"name": "C", "score": 80},
]
ordered = sorted(records, key=lambda row: (-row["score"], row["name"]))
print([row["name"] for row in ordered])
