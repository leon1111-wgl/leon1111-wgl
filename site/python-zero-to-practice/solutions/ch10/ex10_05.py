# 第 10_05 题 所有项均有效
# 实现 all_positive(values)，必须非空且每个数字大于 0 才返回 True。依次打印对 [1,2] 和 [] 的结果。
# 预期程序输出：
# True
# False

def all_positive(values):
    return bool(values) and all(value > 0 for value in values)

print(all_positive([1, 2]))
print(all_positive([]))
