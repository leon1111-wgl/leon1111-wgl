# 第 05_05 题 找最大值
# 不用 max，求非空列表 [-5, -2, -9] 的最大值，输出 -2。
# 预期程序输出：
# -2

numbers = [-5, -2, -9]
largest = numbers[0]
for number in numbers[1:]:
    if number > largest:
        largest = number
print(largest)
