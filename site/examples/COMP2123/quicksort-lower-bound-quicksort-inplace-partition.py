# Leon | Original learning example
# Partition inside one array
# Python 3.12+ | Run: python quicksort-lower-bound-quicksort-inplace-partition.py
values = [4, 1, 3, 2]
stack = [(0, len(values) - 1)]
while stack:
    low, high = stack.pop()
    if low >= high:
        continue
    pivot = values[high]
    boundary = low
    for scan in range(low, high):
        if values[scan] <= pivot:
            values[boundary], values[scan] = values[scan], values[boundary]
            boundary += 1
    values[boundary], values[high] = values[high], values[boundary]
    print("pivot:", pivot, "index:", boundary, "state:", values)
    stack.append((boundary + 1, high))
    stack.append((low, boundary - 1))
print("sorted:", values)
