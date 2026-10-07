# 第 10_04 题 建立姓名成绩映射
# 实现 make_scores(names, scores)，同长度且姓名唯一时返回字典；长度不同抛 ValueError。打印 ["A","B"] 与 [80,90] 的结果。
# 预期程序输出：
# {'A': 80, 'B': 90}

def make_scores(names, scores):
    return dict(zip(names, scores, strict=True))

print(make_scores(["A", "B"], [80, 90]))
