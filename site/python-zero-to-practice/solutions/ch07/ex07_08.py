# 第 07_08 题 复制二维数表
# original=[[1,2],[3,4]]，用逐行 copy 建立新二维列表，修改新表左上角为 9。依次输出原表、新表。
# 预期程序输出：
# [[1, 2], [3, 4]]
# [[9, 2], [3, 4]]

original = [[1, 2], [3, 4]]
copied = []
for row in original:
    copied.append(row.copy())
copied[0][0] = 9
print(original)
print(copied)
