# 记录整体划分
import random
records = [{"id": i, "label": i % 2} for i in range(6)]
shuffled = records.copy()
random.Random(42).shuffle(shuffled)
train = shuffled[:4]
test = shuffled[4:]
print(len(train), len(test))
print(set(row["id"] for row in train).isdisjoint(row["id"] for row in test))
print([row["id"] for row in records])
