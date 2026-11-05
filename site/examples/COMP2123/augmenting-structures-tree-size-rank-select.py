# Leon | Original learning example
# Rank and select with subtree sizes
# Python 3.12+ | Run: python augmenting-structures-tree-size-rank-select.py
class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.size = 1                       # keys stored in this subtree

def size(node):
    return 0 if node is None else node.size

def insert(node, key):
    if node is None:
        return Node(key)
    if key < node.key:
        node.left = insert(node.left, key)
    elif key > node.key:
        node.right = insert(node.right, key)
    node.size = 1 + size(node.left) + size(node.right)   # repair on the way up
    return node

def rank(node, key):
    """Position key has (or would have) in sorted order, counting from 1."""
    if node is None:
        return 1
    if key <= node.key:
        return rank(node.left, key)
    return size(node.left) + 1 + rank(node.right, key)

def select(node, k, path):
    """The k-th smallest key (k = 1 is the smallest). path records the walk."""
    path.append(node.key)
    left = size(node.left)
    if k <= left:
        return select(node.left, k, path)
    if k == left + 1:
        return node.key
    return select(node.right, k - left - 1, path)

root = None
for key in [40, 20, 60, 10, 30, 50, 70]:
    root = insert(root, key)
print("sizes: root", root.size, " left", root.left.size, " right", root.right.size)

path = []
print("5th smallest:", select(root, 5, path), " walk:", path)
print("rank of 50:", rank(root, 50), " rank of 65:", rank(root, 65))
print("keys in [25, 56):", rank(root, 56) - rank(root, 25))
