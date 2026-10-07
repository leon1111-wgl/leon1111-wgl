# Leon | Original learning example
# Insert keys and record the search route
# Python 3.12+ | Run: python bst-range-queries-bst-build-search.py
class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
def insert(node, key):
    if node is None:
        return Node(key)
    if key < node.key:
        node.left = insert(node.left, key)
    elif key > node.key:
        node.right = insert(node.right, key)
    return node
root = None
for key in [18, 9, 27, 4, 13, 22, 31]:
    root = insert(root, key)
current = root
route = []
while current is not None:
    route.append(current.key)
    if current.key == 22:
        break
    current = current.left if 22 < current.key else current.right
print("route:", route)
print("found:", current is not None)
