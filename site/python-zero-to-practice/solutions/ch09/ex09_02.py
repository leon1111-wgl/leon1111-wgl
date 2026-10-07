# 第 09_02 题 安全平均值
# 实现 mean(values)，非空返回平均值，空列表返回 None，不修改输入。依次打印 mean([60,90]) 与 mean([])。
# 预期程序输出：
# 75.0
# None

def mean(values):
    if not values:
        return None
    return sum(values) / len(values)

print(mean([60, 90]))
print(mean([]))
