# 局部随机性
import random
first = random.Random(42)
second = random.Random(42)
a = [first.random() for _ in range(3)]
b = [second.random() for _ in range(3)]
print(a == b)
print(all(0 <= value < 1 for value in a))
