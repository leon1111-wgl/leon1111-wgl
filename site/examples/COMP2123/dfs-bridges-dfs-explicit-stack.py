# Guoliang | Original learning example
# Explore without recursive calls
# Python 3.12+ | Run: python dfs-bridges-dfs-explicit-stack.py
graph = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": [], "X": []}
stack = ["A"]
seen = set()
order = []
while stack:
    u = stack.pop()
    if u in seen:
        continue
    seen.add(u)
    order.append(u)
    for v in reversed(graph[u]):
        if v not in seen:
            stack.append(v)
print("order:", order)
print("X reachable:", "X" in seen)
