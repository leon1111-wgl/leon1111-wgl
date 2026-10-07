# Leon | Original learning example
# Rotate an outer-heavy branch right
# Python 3.12+ | Run: python avl-balance-avl-single-rotation.py
class Node:
    def __init__(self, key):
        self.key, self.left, self.right, self.height = key, None, None, 0
def height(node):
    return -1 if node is None else node.height
def update(node):
    node.height = 1 + max(height(node.left), height(node.right))
def rotate_right(root):
    new_root = root.left
    root.left = new_root.right
    new_root.right = root
    update(root)
    update(new_root)
    return new_root
root = Node(30)
root.left = Node(20)
root.left.left = Node(10)
update(root.left)
update(root)
print("before height:", root.height)
root = rotate_right(root)
print("keys:", root.left.key, root.key, root.right.key)
print("after height:", root.height)
