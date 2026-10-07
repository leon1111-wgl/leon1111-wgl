# Leon | Original learning example
# Trace shorter routes with a lazy heap
# Python 3.12+ | Run: python dijkstra-relaxation-dijkstra-lazy-heap.py
import heapq
graph = {"S": [("A", 6), ("B", 2)], "B": [("A", 1), ("C", 7)],
         "A": [("C", 3)], "C": []}
distance = {v: float("inf") for v in graph}
distance["S"] = 0
parent = {}
heap = [(0, "S")]
while heap:
    cost, u = heapq.heappop(heap)
    if cost != distance[u]:
        continue
    for v, weight in graph[u]:
        candidate = cost + weight
        if candidate < distance[v]:
            distance[v] = candidate
            parent[v] = u
            heapq.heappush(heap, (candidate, v))
route = ["C"]
while route[-1] != "S":
    route.append(parent[route[-1]])
route.reverse()
print("distances:", [(v, distance[v]) for v in ["S", "A", "B", "C"]])
print("route:", route)
