# Leon | Original learning example
# Greedy, uniform-cost and A* on one graph
# Python 3.12+ | Run: python greedy-best-first-dominance-greedy-uniform-astar-compare.py
from heapq import heappop, heappush

graph = {"S": [("A", 4), ("E", 9)], "A": [("B", 7), ("D", 6)], "B": [("G", 3)],
         "D": [("E", 3)], "E": [("G", 8)], "G": []}
h1 = {"S": 7, "A": 5, "B": 1, "D": 5, "E": 4, "G": 0}    # a rough lower bound
h2 = {"S": 11, "A": 7, "B": 1, "D": 8, "E": 6, "G": 0}   # a tighter lower bound


def best_first(priority):
    """Expand the frontier node with the smallest priority(g, node)."""
    frontier = [(priority(0, "S"), 0, "S", ["S"])]
    done, expanded = set(), []
    while frontier:
        _, g, node, path = heappop(frontier)
        if node in done:
            continue
        done.add(node)
        expanded.append(node)
        if node == "G":
            return expanded, path, g
        for nxt, step in graph[node]:
            if nxt not in done:
                heappush(frontier, (priority(g + step, nxt), g + step, nxt, path + [nxt]))


def true_remaining():
    """h*(n): the real cheapest cost from n to G (every edge goes 'forward')."""
    cost = {"G": 0}
    for node in ["E", "B", "D", "A", "S"]:
        cost[node] = min(step + cost[nxt] for nxt, step in graph[node])
    return cost


star = true_remaining()
for name, h in (("h1", h1), ("h2", h2)):
    admissible = all(h[n] <= star[n] for n in graph)
    consistent = all(h[a] <= step + h[b] for a in graph for b, step in graph[a])
    print(f"{name}: admissible={admissible} consistent={consistent}")
print("h2 dominates h1:", all(h2[n] >= h1[n] for n in graph))

runs = [("greedy (h2)", lambda g, n: h2[n]),
        ("uniform-cost", lambda g, n: g),
        ("A* with h1", lambda g, n: g + h1[n]),
        ("A* with h2", lambda g, n: g + h2[n])]
for name, priority in runs:
    expanded, path, cost = best_first(priority)
    print(f"{name:<13} expanded {len(expanded)}: {' '.join(expanded):<13} path {''.join(path):<5} cost {cost}")

# Two different lower bounds: neither one is above the other at every node.
ha = {"S": 8, "A": 8, "B": 1, "D": 7, "E": 4, "G": 0}
hb = {"S": 9, "A": 7, "B": 3, "D": 1, "E": 6, "G": 0}
hmax = {n: max(ha[n], hb[n]) for n in graph}
hsum = {n: ha[n] + hb[n] for n in graph}
for name, h in (("ha", ha), ("hb", hb), ("max(ha,hb)", hmax), ("ha+hb", hsum)):
    admissible = all(h[n] <= star[n] for n in graph)
    consistent = all(h[a] <= step + h[b] for a in graph for b, step in graph[a])
    print(f"{name:<10} admissible={admissible} consistent={consistent}")
for name, h in (("ha", ha), ("hb", hb), ("max(ha,hb)", hmax)):
    expanded, path, cost = best_first(lambda g, n: g + h[n])
    print(f"A* with {name:<10} expanded {len(expanded)}: {' '.join(expanded)}")
print("ha+hb is above the true remaining cost at:",
      " ".join(n for n in graph if hsum[n] > star[n]))
