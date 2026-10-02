# Guoliang | Original learning example
# Separate membership from multiplicity
# Python 3.12+ | Run: python cuckoo-maps-sets-set-and-counter-contracts.py
from collections import Counter
colors = ["red", "blue", "red"]
members = set(colors)
counts = Counter(colors)
print("red present:", "red" in members)
print("distinct:", len(members))
print("red count:", counts["red"])
print("total:", sum(counts.values()))
