# Guoliang | Original learning example
# Find a bridge with discovery and low values
# Python 3.12+ | Run: python dfs-bridges-dfs-low-bridge-trace.py
graph = {"A": ["B", "C"], "B": ["A", "C"],
         "C": ["B", "A", "D"], "D": ["C"]}
discovery = {}
low = {}
bridges = []
def dfs(u, parent=None):
    discovery[u] = len(discovery)
    low[u] = discovery[u]
    for v in graph[u]:
        if v == parent:
            continue
        if v not in discovery:
            dfs(v, u)
            low[u] = min(low[u], low[v])
            if low[v] > discovery[u]:
                bridges.append((u, v))
        else:
            low[u] = min(low[u], discovery[v])
for vertex in graph:
    if vertex not in discovery:
        dfs(vertex)
print("discovery:", discovery)
print("low:", low)
print("bridges:", bridges)
