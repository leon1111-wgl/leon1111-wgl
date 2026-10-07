# Leon | Original learning example
# Check ties with the dominance definition
# Python 3.12+ | Run: python pareto-maxima-pareto-pairwise-oracle.py
points = [("A", 3, 5), ("B", 3, 5), ("C", 3, 4), ("D", 2, 6)]
def dominates(p, q):
    return p[1] >= q[1] and p[2] >= q[2] and (p[1] > q[1] or p[2] > q[2])
frontier = []
for candidate in points:
    blocked = any(dominates(other, candidate) for other in points)
    if not blocked:
        frontier.append(candidate[0])
print("frontier:", frontier)
print("A dominates B:", dominates(points[0], points[1]))
print("A dominates C:", dominates(points[0], points[2]))
