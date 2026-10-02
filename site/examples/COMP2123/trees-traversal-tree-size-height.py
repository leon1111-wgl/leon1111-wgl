# Guoliang | Original learning example
# Calculate size and height together
# Python 3.12+ | Run: python trees-traversal-tree-size-height.py
tree = ("R", ("A", ("C", None, None), None), ("B", None, None))
def facts(node):
    if node is None:
        return 0, -1
    _, left, right = node
    left_size, left_height = facts(left)
    right_size, right_height = facts(right)
    return 1 + left_size + right_size, 1 + max(left_height, right_height)

size, height = facts(tree)
print("size:", size)
print("height:", height)
print("empty:", facts(None))
