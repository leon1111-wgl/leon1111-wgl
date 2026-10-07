# Leon | Original learning example
# Fill a capacity by density
# Python 3.12+ | Run: python greedy-fractional-fractional-knapsack-trace.py
items = [("A", 4, 28), ("B", 5, 25), ("C", 6, 18)]
remaining = 10
total = 0.0
for name, weight, value in sorted(items, key=lambda item: item[2] / item[1], reverse=True):
    taken_weight = min(weight, remaining)
    fraction = taken_weight / weight
    total += fraction * value
    remaining -= taken_weight
    print(name, "weight:", taken_weight, "fraction:", round(fraction, 3))
    if remaining == 0:
        break
print("total value:", total)
