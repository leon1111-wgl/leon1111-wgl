# Leon | Original learning example
# Check where a greedy proof stops working
# Python 3.12+ | Run: python greedy-fractional-indivisible-knapsack-counterexample.py
from itertools import product
items = [("A", 3, 5), ("B", 2, 3), ("C", 2, 3)]
capacity = 4
remaining = capacity
greedy = []
for name, weight, value in sorted(items, key=lambda x: x[2] / x[1], reverse=True):
    if weight <= remaining:
        greedy.append(name)
        remaining -= weight
best_value = -1
best_names = []
for mask in product([0, 1], repeat=len(items)):
    weight = sum(take * item[1] for take, item in zip(mask, items))
    value = sum(take * item[2] for take, item in zip(mask, items))
    if weight <= capacity and value > best_value:
        best_value = value
        best_names = [item[0] for take, item in zip(mask, items) if take]
print("density choice:", greedy)
print("best whole items:", best_names)
print("best value:", best_value)
