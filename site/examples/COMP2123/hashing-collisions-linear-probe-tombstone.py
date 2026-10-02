# Guoliang | Original learning example
# Delete without breaking a probe chain
# Python 3.12+ | Run: python hashing-collisions-linear-probe-tombstone.py
deleted = object()
table = [None] * 7
for key in [10, 17, 24]:
    index = key % 7
    while table[index] is not None:
        index = (index + 1) % 7
    table[index] = key
table[4] = deleted
def contains(key):
    visited = []
    for offset in range(len(table)):
        index = (key % 7 + offset) % 7
        visited.append(index)
        item = table[index]
        if item is None:
            return False, visited
        if item is not deleted and item == key:
            return True, visited
    return False, visited
print(contains(24))
table[4] = None
print(contains(24))
