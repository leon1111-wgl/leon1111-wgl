# Guoliang | Original learning example
# Implement merge sort from its stopping case
# Python 3.12+ | Run: python recurrences-merge-sort-merge-sort-real-merge.py
def merge_sort(values):
    if len(values) <= 1:
        return values.copy()
    middle = len(values) // 2
    left = merge_sort(values[:middle])
    right = merge_sort(values[middle:])
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
print(merge_sort([8, 3, 7, 1]))
print(merge_sort([]))
print(merge_sort([4, 2, 4]))
