# 第 10_01 题 平方正数
# 实现 positive_squares(values)，返回正数的平方列表，保持顺序；打印对 [-2,0,3] 的结果。
# 预期程序输出：
# [9]

def positive_squares(values):
    return [value ** 2 for value in values if value > 0]

print(positive_squares([-2, 0, 3]))
