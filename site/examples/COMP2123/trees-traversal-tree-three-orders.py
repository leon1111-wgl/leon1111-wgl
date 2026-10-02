# Guoliang | Original learning example
# Compare three traversal orders
# Python 3.12+ | Run: python trees-traversal-tree-three-orders.py
tree = ("R", ("A", ("C", None, None), None), ("B", None, None))
def walk(node, order):
    if node is None:
        return []
    value, left, right = node
    first = walk(left, order)
    last = walk(right, order)
    if order == "pre":
        return [value] + first + last
    if order == "in":
        return first + [value] + last
    return first + last + [value]

for order in ["pre", "in", "post"]:
    print(order, walk(tree, order))
