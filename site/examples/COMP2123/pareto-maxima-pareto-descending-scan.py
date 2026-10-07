# Leon | Original learning example
# Keep points that improve the best second score
# Python 3.12+ | Run: python pareto-maxima-pareto-descending-scan.py
points = [("A", 1, 8), ("B", 3, 5), ("C", 4, 7),
          ("D", 6, 4), ("E", 7, 2)]
ordered = sorted(points, key=lambda p: (p[1], p[2]), reverse=True)
best_y = float("-inf")
frontier = []
for name, x, y in ordered:
    if y > best_y:
        frontier.append(name)
        best_y = y
    print(name, "best y:", best_y)
print("frontier:", frontier)
