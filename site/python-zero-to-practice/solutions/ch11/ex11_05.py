# 第 11_05 题 复现实验打乱
# 列表 range(5)，分别复制两份并用两个 random.Random(7) 打乱，输出两份是否相同 True，再输出原列表。
# 预期程序输出：
# True
# [0, 1, 2, 3, 4]

import random
original = list(range(5))
a = original.copy()
b = original.copy()
random.Random(7).shuffle(a)
random.Random(7).shuffle(b)
print(a == b)
print(original)
