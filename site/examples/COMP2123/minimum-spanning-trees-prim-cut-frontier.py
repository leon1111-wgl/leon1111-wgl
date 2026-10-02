# Guoliang | Original learning example
# Grow a minimum spanning tree across a cut
# Python 3.12+ | Run: python minimum-spanning-trees-prim-cut-frontier.py
import heapq
graph = {"A": [("B", 1), ("C", 4)], "B": [("A", 1), ("C", 2), ("D", 6)],
         "C": [("A", 4), ("B", 2), ("D", 3)], "D": [("B", 6), ("C", 3)]}
visited = {"A"}
heap = [(w, "A", v) for v, w in graph["A"]]
heapq.heapify(heap)
chosen = []
total = 0
while heap:
    weight, u, v = heapq.heappop(heap)
    if v in visited:
        continue
    visited.add(v)
    chosen.append((u, v, weight))
    total += weight
    for neighbor, cost in graph[v]:
        if neighbor not in visited:
            heapq.heappush(heap, (cost, v, neighbor))
print("edges:", chosen)
print("total:", total)
print("spans graph:", len(visited) == len(graph))
