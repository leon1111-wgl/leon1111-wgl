# 第 11_02 题 词频最多者
# 用 Counter 统计 "red blue red green red blue"，输出 most_common(1) 的结果。
# 预期程序输出：
# [('red', 3)]

from collections import Counter
counts = Counter("red blue red green red blue".split())
print(counts.most_common(1))
