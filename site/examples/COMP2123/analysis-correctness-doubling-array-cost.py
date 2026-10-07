# Leon | Original learning example
# Count the cost of growing storage
# Python 3.12+ | Run: python analysis-correctness-doubling-array-cost.py
capacity = 1
size = 0
copies = 0
for value in [10, 20, 30, 40, 50]:
    if size == capacity:
        copies += size
        capacity *= 2
    size += 1
    print("size:", size, "capacity:", capacity, "copies:", copies)
print("writes plus copies:", size + copies)
