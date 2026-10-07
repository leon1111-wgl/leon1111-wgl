# Leon | Original learning example
# A running total and its invariant
# Python 3.12+ | Run: python analysis-correctness-prefix-total-trace.py
values = [4, -1, 6, 2]
total = 0
prefixes = []
for value in values:
    total += value
    prefixes.append(total)
    print(value, total)
print(prefixes)
