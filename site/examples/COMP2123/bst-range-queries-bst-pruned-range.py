# Guoliang | Original learning example
# Report a range without visiting every branch
# Python 3.12+ | Run: python bst-range-queries-bst-pruned-range.py
tree = (18, (9, (4, None, None), (13, None, None)),
            (27, (22, None, None), (31, None, None)))
def report(node, low, high, result):
    if node is None:
        return
    key, left, right = node
    if low < key:
        report(left, low, high, result)
    if low <= key <= high:
        result.append(key)
    if key < high:
        report(right, low, high, result)
result = []
report(tree, 10, 28, result)
print(result)
