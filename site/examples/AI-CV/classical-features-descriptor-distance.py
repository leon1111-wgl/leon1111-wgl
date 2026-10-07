# Leon | Original learning example
# Compare two patch descriptions
# Python 3.12+ | Run: python classical-features-descriptor-distance.py
import math
query = (1, 2)
candidates = {"A": (1, 3), "B": (4, 6)}
def distance(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))
ranked = sorted((distance(query, value), name) for name, value in candidates.items())
ratio = ranked[0][0] / ranked[1][0]
print("ranked:", ranked)
print(f"ratio={ratio:.2f}; accept={ratio < 0.8}")
