# 第 13_03 题 正批大小
# 实现 batch_count(total, size)，假定 total 为非负整数，size 为整数；size<=0 抛 ValueError，否则向上取整计算批次数。打印 batch_count(17,8)。
# 预期程序输出：
# 3

def batch_count(total, size):
    if size <= 0:
        raise ValueError("size 必须为正数")
    return (total + size - 1) // size

print(batch_count(17, 8))
