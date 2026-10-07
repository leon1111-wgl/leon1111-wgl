# 第 05_02 题 偶数总和
# 计算 1 到 20 之间所有偶数的和，输出 110。
# 预期程序输出：
# 110

total = 0
for number in range(2, 21, 2):
    total += number
print(total)
