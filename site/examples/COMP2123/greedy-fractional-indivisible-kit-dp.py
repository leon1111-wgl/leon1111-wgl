# Leon | Original learning example
# When greedy fails: pack whole science kits
# Python 3.12+ | Run: python greedy-fractional-indivisible-kit-dp.py
def knapsack(items, capacity):
    if not isinstance(capacity, int) or capacity < 0:
        raise ValueError("capacity must be a nonnegative integer")
    if any(not isinstance(w, int) or w <= 0 or v < 0 for _, w, v in items):
        raise ValueError("positive integer weights and nonnegative values required")
    n = len(items)
    best = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i, (_, weight, value) in enumerate(items, 1):
        for room in range(capacity + 1):
            best[i][room] = best[i - 1][room]
            if weight <= room:
                take = value + best[i - 1][room - weight]
                best[i][room] = max(best[i][room], take)
    chosen, room = [], capacity
    for i in range(n, 0, -1):
        if best[i][room] != best[i - 1][room]:
            name, weight, _ = items[i - 1]
            chosen.append(name)
            room -= weight
    return best[n][capacity], list(reversed(chosen)), best

items = [("A", 3, 5), ("B", 2, 3), ("C", 2, 3)]
value, chosen, table = knapsack(items, 4)
assert (value, chosen) == (6, ["B", "C"])
assert knapsack(items, 0)[0] == 0
assert knapsack([], 4)[0] == 0
for i, row in enumerate(table):
    print(f"first {i} kits: {row}")
print("selected:", chosen, "value:", value)
