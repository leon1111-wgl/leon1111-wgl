# Leon | Original learning example
# Choose a minimum without a heap
# Python 3.12+ | Run: python dijkstra-relaxation-dijkstra-array-choice.py
graph = {"S": [("A", 0), ("B", 5)], "A": [("B", 2)], "B": [], "X": []}
distance = {v: float("inf") for v in graph}
distance["S"] = 0
settled = set()
while True:
    candidates = [v for v in graph if v not in settled]
    if not candidates:
        break
    u = min(candidates, key=lambda v: distance[v])
    if distance[u] == float("inf"):
        break
    settled.add(u)
    print("settled:", u, distance[u])
    for v, weight in graph[u]:
        distance[v] = min(distance[v], distance[u] + weight)
print("X:", distance["X"])
