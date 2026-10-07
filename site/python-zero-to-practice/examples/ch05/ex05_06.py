# 空列表平均值
scores = []
total = 0
for score in scores:
    total += score
if len(scores) == 0:
    print("没有成绩")
else:
    print(total / len(scores))
