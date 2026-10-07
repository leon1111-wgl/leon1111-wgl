# Leon | Original learning example
# Watch insertion sort grow a prefix
# Python 3.12+ | Run: python sorting-baselines-insertion-sort-trace.py
values = [5, 2, 4, 1]
shifts = 0
for i in range(1, len(values)):
    item = values[i]
    j = i - 1
    while j >= 0 and values[j] > item:
        values[j + 1] = values[j]
        j -= 1
        shifts += 1
    values[j + 1] = item
    print(values)
print("shifts:", shifts)
