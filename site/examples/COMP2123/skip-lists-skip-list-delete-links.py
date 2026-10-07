# Leon | Original learning example
# Remove a key from every level it occupies
# Python 3.12+ | Run: python skip-lists-skip-list-delete-links.py
class Node:
    def __init__(self, key, levels):
        self.key = key
        self.forward = [None] * levels
head = Node(None, 2)
a, b, c = Node(3, 2), Node(8, 1), Node(11, 2)
head.forward = [a, a]
a.forward = [b, c]
b.forward = [c]
def delete(key):
    before = [head] * 2
    current = head
    for layer in [1, 0]:
        while current.forward[layer] is not None and current.forward[layer].key < key:
            current = current.forward[layer]
        before[layer] = current
    target = before[0].forward[0]
    if target is None or target.key != key:
        return False
    for layer in range(len(target.forward)):
        before[layer].forward[layer] = target.forward[layer]
    return True
def keys(layer):
    result = []
    current = head.forward[layer]
    while current is not None:
        result.append(current.key)
        current = current.forward[layer]
    return result
print("delete 3:", delete(3))
print("base:", keys(0))
print("upper:", keys(1))
print("delete 7:", delete(7))
