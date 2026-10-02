# Guoliang | Original learning example
# Expose a nearly plausible biased shuffle
# Python 3.12+ | Run: python random-permutations-biased-shuffle-audit.py
from itertools import product
from collections import Counter
outcomes = Counter()
for choices in product(range(3), repeat=3):
    cards = ["A", "B", "C"]
    for i, j in enumerate(choices):
        cards[i], cards[j] = cards[j], cards[i]
    outcomes["".join(cards)] += 1
for order in sorted(outcomes):
    print(order, outcomes[order])
print("paths:", sum(outcomes.values()))
print("equal frequencies:", len(set(outcomes.values())) == 1)
