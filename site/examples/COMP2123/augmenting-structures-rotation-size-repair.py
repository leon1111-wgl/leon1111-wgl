# Leon | Original learning example
# A rotation must repair sizes
# Python 3.12+ | Run: python augmenting-structures-rotation-size-repair.py
class Node:
    def __init__(self, key, left=None, right=None):
        self.key, self.left, self.right = key, left, right
        self.size = 1 + (left.size if left else 0) + (right.size if right else 0)

def size(node):
    return 0 if node is None else node.size

def true_count(node):
    """Slow checker: count the nodes by visiting all of them."""
    return 0 if node is None else 1 + true_count(node.left) + true_count(node.right)

def inorder(node):
    return [] if node is None else inorder(node.left) + [node.key] + inorder(node.right)

root = Node(30, Node(20, Node(10)))
print("before: root", root.key, " size", root.size, " inorder", inorder(root))

top = root.left                              # rotate right at 30
root.left = top.right
top.right = root
print("links changed, sizes not yet repaired:")
print("  new root", top.key, " stored size", top.size, " true size", true_count(top))

root.size = 1 + size(root.left) + size(root.right)   # lower node first
top.size = 1 + size(top.left) + size(top.right)      # then the new top
print("after repair: new root", top.key, " stored size", top.size, " true size", true_count(top))
print("old root", root.key, " size", root.size, " inorder", inorder(top))
