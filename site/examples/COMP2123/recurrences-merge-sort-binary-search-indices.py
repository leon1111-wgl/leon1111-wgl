# Leon | Original learning example
# Halve a search interval without copying data
# Python 3.12+ | Run: python recurrences-merge-sort-binary-search-indices.py
values = [2, 5, 8, 12, 16, 23, 38]
target = 16
low, high = 0, len(values) - 1
checked = []
found = -1
while low <= high:
    middle = (low + high) // 2
    checked.append(values[middle])
    if values[middle] == target:
        found = middle
        break
    if values[middle] < target:
        low = middle + 1
    else:
        high = middle - 1
print("checked:", checked)
print("index:", found)
