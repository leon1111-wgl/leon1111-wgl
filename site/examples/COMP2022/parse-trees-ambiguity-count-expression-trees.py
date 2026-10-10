# Leon | Original learning example
# Count parse trees instead of assuming one
# Python 3.12+ | Run: python parse-trees-ambiguity-count-expression-trees.py
from functools import lru_cache

def count_trees(operands):
    if operands < 1:
        raise ValueError("at least one operand required")
    ways = [0] * (operands + 1)
    ways[1] = 1
    for size in range(2, operands + 1):
        ways[size] = sum(ways[left] * ways[size - left]
                         for left in range(1, size))
    return ways[operands]

@lru_cache(None)
def trees(operands):
    if operands == 1:
        return ("n",)
    return tuple(f"({left}+{right})"
                 for cut in range(1, operands)
                 for left in trees(cut)
                 for right in trees(operands - cut))

assert [count_trees(n) for n in range(1, 6)] == [1, 1, 2, 5, 14]
assert len(set(trees(4))) == count_trees(4)
print("four operands:", count_trees(4), "parse trees")
for tree in trees(4):
    print(tree)
