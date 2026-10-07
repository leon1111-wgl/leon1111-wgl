# 配对与序号
names = ["A", "B"]
scores = [80, 90]
for index, (name, score) in enumerate(zip(names, scores, strict=True), start=1):
    print(index, name, score)
