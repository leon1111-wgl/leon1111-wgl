# 第 15_04 题 生成器消费观察
# 建立 (x*x for x in range(3))，连续两次 print(list(g))，写出结果并解释。
# 预期程序输出：
# [0, 1, 4]
# []

g = (x * x for x in range(3))
print(list(g))
print(list(g))
