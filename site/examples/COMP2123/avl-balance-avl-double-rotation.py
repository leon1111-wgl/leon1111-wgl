# Guoliang | Original learning example
# Repair an inner-heavy branch
# Python 3.12+ | Run: python avl-balance-avl-double-rotation.py
class Node:
    def __init__(self, key, left=None, right=None):
        self.key, self.left, self.right = key, left, right
def rotate_left(root):
    top = root.right
    root.right = top.left
    top.left = root
    return top
def rotate_right(root):
    top = root.left
    root.left = top.right
    top.right = root
    return top
root = Node(30, Node(10, right=Node(20)))
root.left = rotate_left(root.left)
print("after first:", root.key, root.left.key, root.left.left.key)
root = rotate_right(root)
print("after second:", root.left.key, root.key, root.right.key)
