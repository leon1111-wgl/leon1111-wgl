# 第 06_06 题 修复 continue 死循环
# 写 while 输出 1 到 5 中的奇数，每个一行；确保遇到偶数也会推进计数器。
# 预期程序输出：
# 1
# 3
# 5

n = 0
while n < 5:
    n += 1
    if n % 2 == 0:
        continue
    print(n)
