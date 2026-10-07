# Leon | Original learning example
# Move both box corners
# Python 3.12+ | Run: python geometry-augmentation-move-box.py
corners = [(10, 20), (30, 50)]
moved = [(2 * x + 5, 2 * y - 3) for x, y in corners]
(x1, y1), (x2, y2) = moved
print("corners:", moved)
print("area:", (x2 - x1) * (y2 - y1))
print("clipped bottom:", min(y2, 80))
