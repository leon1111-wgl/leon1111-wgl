# Guoliang | Original learning example
# Partition and recursively sort both sides
# Python 3.12+ | Run: python quicksort-lower-bound-quicksort-three-way.py
def quicksort(values):
    if len(values) <= 1:
        return values.copy()
    pivot = values[0]
    smaller, equal, larger = [], [], []
    for value in values:
        if value < pivot:
            smaller.append(value)
        elif value > pivot:
            larger.append(value)
        else:
            equal.append(value)
    return quicksort(smaller) + equal + quicksort(larger)
print(quicksort([9, 2, 7, 4, 6, 4]))
print(quicksort([5, 5, 5]))
