# Guoliang | Original learning example
# Build real forward-link towers
# Python 3.12+ | Run: python skip-lists-skip-list-links-and-insert.py
class Node:
    def __init__(self, key, level):
        self.key = key
        self.forward = [None] * (level + 1)
head = Node(None, 2)
def insert(key, level):
    before = [head] * 3
    current = head
    for layer in range(2, -1, -1):
        while current.forward[layer] is not None and current.forward[layer].key < key:
            current = current.forward[layer]
        before[layer] = current
    node = Node(key, level)
    for layer in range(level + 1):
        node.forward[layer] = before[layer].forward[layer]
        before[layer].forward[layer] = node
def keys(layer):
    result = []
    current = head.forward[layer]
    while current is not None:
        result.append(current.key)
        current = current.forward[layer]
    return result
for key, level in [(3, 1), (8, 0), (11, 2), (17, 0), (24, 1), (29, 0)]:
    insert(key, level)
for layer in [2, 1, 0]:
    print("level", layer, keys(layer))
current = head
moves = []
for layer in range(2, -1, -1):
    while current.forward[layer] is not None and current.forward[layer].key < 17:
        current = current.forward[layer]
        moves.append((layer, current.key))
candidate = current.forward[0]
print("right moves:", moves)
print("found 17:", candidate is not None and candidate.key == 17)
insert(20, 1)
print("after insert:", keys(0))
