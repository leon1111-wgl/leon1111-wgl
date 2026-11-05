# Leon | Original learning example
# Model a free ticket as extra state
# Python 3.12+ | Run: python augmenting-structures-ticket-state-graph.py
import heapq

roads = [("S", "A", 2), ("A", "T", 9), ("A", "C", 1),
         ("S", "B", 4), ("B", "C", 3), ("C", "T", 4)]
graph = {}
for u, v, w in roads:
    graph.setdefault(u, []).append((v, w))
    graph.setdefault(v, []).append((u, w))

def cheapest(source, target, tickets):
    """Dijkstra over states (town, tickets still unused)."""
    start = (source, tickets)
    best = {start: 0}
    parent = {}
    heap = [(0, start)]
    while heap:
        cost, state = heapq.heappop(heap)
        if cost > best[state]:
            continue                                   # stale heap entry
        town, left = state
        moves = [((nxt, left), cost + w) for nxt, w in graph[town]]
        if left > 0:                                   # use a ticket: free road
            moves += [((nxt, left - 1), cost) for nxt, w in graph[town]]
        for new_state, new_cost in moves:
            if new_cost < best.get(new_state, float("inf")):
                best[new_state] = new_cost
                parent[new_state] = state
                heapq.heappush(heap, (new_cost, new_state))
    end = min((s for s in best if s[0] == target), key=lambda s: best[s])
    route = [end]
    while route[-1] != start:
        route.append(parent[route[-1]])
    return best[end], route[::-1]

for tickets in [0, 1, 2]:
    cost, route = cheapest("S", "T", tickets)
    print("tickets", tickets, "-> cost", cost, " states:", route)

cost, route = cheapest("S", "T", 0)
weights = {(u, v): w for u, v, w in roads}
weights.update({(v, u): w for u, v, w in roads})
biggest = max(weights[(a[0], b[0])] for a, b in zip(route, route[1:]))
print("plan first, discount the dearest road later:", cost - biggest)
