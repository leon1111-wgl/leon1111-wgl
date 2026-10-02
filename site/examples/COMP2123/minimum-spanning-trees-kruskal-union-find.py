# Guoliang | Original learning example
# Build an MST with union-find
# Python 3.12+ | Run: python minimum-spanning-trees-kruskal-union-find.py
vertices = ["A", "B", "C", "D"]
edges = [(1, "A", "B"), (2, "B", "C"), (4, "A", "C"),
         (3, "C", "D"), (6, "B", "D")]
parent = {v: v for v in vertices}
size = {v: 1 for v in vertices}
def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x
chosen = []
total = 0
for weight, u, v in sorted(edges):
    a, b = find(u), find(v)
    if a == b:
        continue
    if size[a] < size[b]:
        a, b = b, a
    parent[b] = a
    size[a] += size[b]
    chosen.append((u, v, weight))
    total += weight
print("edges:", chosen)
print("total:", total)
