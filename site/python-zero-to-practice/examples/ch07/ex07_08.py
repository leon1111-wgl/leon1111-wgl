# 列表筛选：为什么连续的负数漏掉一个
values = [-2, -1, 0, 4]
wrong = values.copy()
visited = []
for value in wrong:
    visited.append(value)
    if value < 0:
        wrong.remove(value)

kept = []
for value in values:
    if value >= 0:
        kept.append(value)

print("错误遍历访问：", visited)
print("错误结果：", wrong)
print("保留结果：", kept)
print("原输入：", values)
