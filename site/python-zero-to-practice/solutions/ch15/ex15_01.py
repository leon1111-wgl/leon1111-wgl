# 第 15_01 题 偶数生成器
# 实现 even_numbers(stop)，使用 yield 产生 0 到 stop 之前的偶数，stop 为非负整数。打印 list(even_numbers(7))。
# 预期程序输出：
# [0, 2, 4, 6]

def even_numbers(stop):
    for number in range(0, stop, 2):
        yield number

print(list(even_numbers(7)))
