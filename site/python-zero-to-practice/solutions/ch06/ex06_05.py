# 第 06_05 题 二维坐标
# 输出两行三列的所有坐标，行与列都从 0 开始，顺序为 0 0 到 1 2，每对一行。
# 预期程序输出：
# 0 0
# 0 1
# 0 2
# 1 0
# 1 1
# 1 2

for row in range(2):
    for column in range(3):
        print(row, column)
