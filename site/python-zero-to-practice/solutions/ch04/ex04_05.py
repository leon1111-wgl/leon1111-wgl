# 第 04_05 题 找三个数最大值
# a=7，b=12，c=9，不用 max，输出最大值 12。
# 预期程序输出：
# 12

a, b, c = 7, 12, 9
largest = a
if b > largest:
    largest = b
if c > largest:
    largest = c
print(largest)
