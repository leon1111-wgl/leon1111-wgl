# 第 06_07 题 整数各位求和
# 对非负整数 2048，用 while、// 和 % 求各位数字之和，输出 14。
# 预期程序输出：
# 14

number = 2048
total = 0
while number > 0:
    total += number % 10
    number //= 10
print(total)
