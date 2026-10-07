# Leon | Original learning example
# Choose a pivot from small-group medians
# Python 3.12+ | Run: python selection-pivots-median-of-medians-select.py
def select(values, rank):
    if not 1 <= rank <= len(values):
        raise ValueError("rank outside list")
    if len(values) <= 5:
        return sorted(values)[rank - 1]
    groups = [values[i:i + 5] for i in range(0, len(values), 5)]
    medians = [sorted(group)[len(group) // 2] for group in groups]
    pivot = select(medians, (len(medians) + 1) // 2)
    lower = [x for x in values if x < pivot]
    equal = [x for x in values if x == pivot]
    higher = [x for x in values if x > pivot]
    if rank <= len(lower):
        return select(lower, rank)
    if rank <= len(lower) + len(equal):
        return pivot
    return select(higher, rank - len(lower) - len(equal))
values = [12, 3, 9, 5, 7, 1, 10, 8, 2, 6, 11, 4]
print("sixth:", select(values, 6))
print("last:", select(values, 12))
print("duplicates:", select([4, 4, 4, 1, 2, 5, 6], 4))
