# Leon | Original learning example
# Handle a negative edge with Bellman–Ford
# Python 3.12+ | Run: python dijkstra-relaxation-negative-edge-relaxation.py
from math import inf

def bellman_ford(nodes, edges, source):
    distance = {node: inf for node in nodes}
    distance[source] = 0
    history = [distance.copy()]
    for _ in range(len(nodes) - 1):
        next_distance = distance.copy()
        for u, v, cost in edges:
            if distance[u] != inf:
                next_distance[v] = min(next_distance[v], distance[u] + cost)
        history.append(next_distance.copy())
        if next_distance == distance:
            break
        distance = next_distance
    if any(distance[u] != inf and distance[u] + w < distance[v]
           for u, v, w in edges):
        raise ValueError("reachable negative cycle")
    return distance, history

nodes = ["S", "A", "B", "C", "Z"]
edges = [("S", "A", 4), ("S", "B", 5), ("A", "B", -2),
         ("B", "C", 3), ("Z", "Z", -1)]
distance, history = bellman_ford(nodes, edges, "S")
assert distance == {"S": 0, "A": 4, "B": 2, "C": 5, "Z": inf}
for k, row in enumerate(history[:4]):
    print(f"at most {k} edges:", [row[v] for v in nodes[:4]])
print("Z is unreachable:", distance["Z"] == inf)
try:
    bellman_ford(nodes, edges + [("C", "A", -6)], "S")
except ValueError as error:
    print(error)
