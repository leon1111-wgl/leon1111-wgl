# 第 10_03 题 负值截为零
# 实现 replace_negative(values)，负数变 0，其他数不变。打印对 [-2,0,5] 的结果。
# 预期程序输出：
# [0, 0, 5]

def replace_negative(values):
    return [0 if value < 0 else value for value in values]

print(replace_negative([-2, 0, 5]))
