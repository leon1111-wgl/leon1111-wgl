# Guoliang | Original learning example
# Find distance to the nearest starting point
# Python 3.12+ | Run: python bfs-distance-multi-source-bfs.py
from collections import deque
graph = {0: [1], 1: [0, 2], 2: [1, 3], 3: [2, 4], 4: [3]}
sources = [0, 4]
distance = {v: None for v in graph}
queue = deque()
for source in sources:
    distance[source] = 0
    queue.append(source)
while queue:
    u = queue.popleft()
    for v in graph[u]:
        if distance[v] is None:
            distance[v] = distance[u] + 1
            queue.append(v)
print("nearest distances:", [distance[v] for v in range(5)])
