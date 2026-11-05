# 配对追踪：默认 zip 漏掉了谁
names = ["小青", "小岩"]
scores = [72]
pairs = list(zip(names, scores))
print("默认配对：", pairs)
print("原条数与配对数：", len(names), len(scores), len(pairs))
if len(names) != len(scores):
    print("拒绝继续：姓名与分数条数不同")
else:
    print("条数一致：", list(zip(names, scores, strict=True)))
