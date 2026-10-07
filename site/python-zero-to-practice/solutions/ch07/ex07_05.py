# 第 07_05 题 二维求和
# grid = [[1,2,3],[4,5,6]]，输出所有数字的总和 21。
# 预期程序输出：
# 21

grid = [[1, 2, 3], [4, 5, 6]]
total = 0
for row in grid:
    for value in row:
        total += value
print(total)
