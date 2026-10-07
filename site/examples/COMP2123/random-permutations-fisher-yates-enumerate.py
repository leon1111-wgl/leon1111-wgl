# Leon | Original learning example
# Check every shuffle path for three cards
# Python 3.12+ | Run: python random-permutations-fisher-yates-enumerate.py
from itertools import product
from collections import Counter
outcomes = Counter()
for choices in product(range(3), range(2)):
    cards = ["A", "B", "C"]
    for i, j in zip([2, 1], choices):
        cards[i], cards[j] = cards[j], cards[i]
    outcomes["".join(cards)] += 1
for order in sorted(outcomes):
    print(order, outcomes[order])
print("paths:", sum(outcomes.values()))
