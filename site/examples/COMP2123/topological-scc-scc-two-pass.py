# Leon | Original learning example
# Find strongly connected components in two passes
# Python 3.12+ | Run: python topological-scc-scc-two-pass.py
def explore(graph, u, seen, out):
    seen.add(u)
    for v in graph[u]:
        if v not in seen:
            explore(graph, v, seen, out)
    out.append(u)                           # u finishes after everything below it

def transpose(graph):
    flipped = {u: [] for u in graph}
    for u in graph:
        for v in graph[u]:
            flipped[v].append(u)            # reverse the edge u -> v
    return flipped

def strongly_connected(graph):
    seen, finish = set(), []
    for u in graph:                         # pass 1: DFS on the original graph
        if u not in seen:
            explore(graph, u, seen, finish)
    print("finishing order:", finish)
    flipped = transpose(graph)
    seen, components = set(), []
    for u in reversed(finish):              # pass 2: DFS on the transpose
        if u not in seen:
            members = []
            explore(flipped, u, seen, members)
            components.append(sorted(members))
    return components

roads = {
    "A": ["B"], "B": ["A"],
    "C": ["D", "A"], "D": ["C", "B"],
    "E": ["F", "C"], "F": ["G"], "G": ["E", "D"],
}
print("components:", strongly_connected(roads))
