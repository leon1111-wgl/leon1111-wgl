# 第 10_06 题 展开二维列表
# 实现 flatten(rows)，按行展开一层二维列表。打印 [[1,2],[],[3]] 的结果 [1,2,3]。
# 预期程序输出：
# [1, 2, 3]

def flatten(rows):
    return [value for row in rows for value in row]

print(flatten([[1, 2], [], [3]]))
