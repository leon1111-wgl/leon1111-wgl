# Guoliang | Original learning example
# Use a queue to find distance and a route
# Python 3.12+ | Run: python bfs-distance-bfs-distance-and-route.py
from collections import deque
graph = {"S": ["A", "B"], "A": ["S", "C"], "B": ["S", "D"],
         "C": ["A", "E"], "D": ["B", "E"], "E": ["C", "D"], "X": []}
distance = {vertex: None for vertex in graph}
parent = {"S": None}
distance["S"] = 0
queue = deque(["S"])
while queue:
    u = queue.popleft()
    for v in graph[u]:
        if distance[v] is None:
            distance[v] = distance[u] + 1
            parent[v] = u
            queue.append(v)
route = []
current = "E"
while current is not None:
    route.append(current)
    current = parent[current]
route.reverse()
print("distance to E:", distance["E"])
print("route:", route)
print("distance to X:", distance["X"])
