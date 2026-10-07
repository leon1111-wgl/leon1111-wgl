# 第 08_07 题 按标签统计
# records=[{"label":1},{"label":0},{"label":1}]，输出标签到数量的字典 {1:2,0:1}。
# 预期程序输出：
# {1: 2, 0: 1}

records = [{"label": 1}, {"label": 0}, {"label": 1}]
counts = {}
for record in records:
    label = record["label"]
    counts[label] = counts.get(label, 0) + 1
print(counts)
