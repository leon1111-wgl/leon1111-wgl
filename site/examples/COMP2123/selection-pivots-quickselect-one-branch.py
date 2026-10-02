# Guoliang | Original learning example
# Find a rank without sorting both sides
# Python 3.12+ | Run: python selection-pivots-quickselect-one-branch.py
def select(values, rank):
    if not 1 <= rank <= len(values):
        raise ValueError("rank outside list")
    remaining = values
    while True:
        pivot = remaining[len(remaining) // 2]
        lower = [x for x in remaining if x < pivot]
        equal = [x for x in remaining if x == pivot]
        higher = [x for x in remaining if x > pivot]
        if rank <= len(lower):
            remaining = lower
        elif rank <= len(lower) + len(equal):
            return pivot
        else:
            rank -= len(lower) + len(equal)
            remaining = higher
values = [12, 3, 9, 5, 7, 1, 10]
print("fourth:", select(values, 4))
print("sixth:", select(values, 6))
print("duplicates:", select([7, 2, 7, 9, 7], 3))
