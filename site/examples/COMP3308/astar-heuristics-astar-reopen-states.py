# Leon | Original learning example
# Reopen a state when A* finds a better route
# Python 3.12+ | Run: python astar-heuristics-astar-reopen-states.py
from heapq import heappop, heappush
from math import inf

def astar(graph, heuristic, start, goal):
    best = {start: 0.0}
    parent = {}
    frontier = [(heuristic[start], 0.0, start)]
    expanded = []
    while frontier:
        _, cost, node = heappop(frontier)
        if cost != best[node]:
            continue
        expanded.append(node)
        if node == goal:
            path = [goal]
            while path[-1] != start:
                path.append(parent[path[-1]])
            return cost, list(reversed(path)), expanded
        for nxt, step in graph[node]:
            if step < 0:
                raise ValueError("nonnegative edges required")
            candidate = cost + step
            if candidate < best.get(nxt, inf):
                best[nxt] = candidate
                parent[nxt] = node
                heappush(frontier, (candidate + heuristic[nxt], candidate, nxt))
    return inf, [], expanded

graph = {"S": [("A", 2), ("B", 1)], "A": [("G", 2)],
         "B": [("A", 0.5), ("G", 100)], "G": []}
h = {"S": 3.5, "A": 0, "B": 2.5, "G": 0}
cost, path, expanded = astar(graph, h, "S", "G")
assert cost == 3.5 and path == ["S", "B", "A", "G"]
assert expanded == ["S", "A", "B", "A", "G"]
assert astar(graph, {node: 0 for node in graph}, "S", "G")[0] == cost
print("expanded:", expanded)
print("path:", path)
print(f"cost: {cost:.1f}")
