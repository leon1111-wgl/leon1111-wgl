# Counter 计数
from collections import Counter
counts = Counter("a b a c b a".split())
print(counts["a"])
print(counts["missing"])
print(counts.most_common(2))
