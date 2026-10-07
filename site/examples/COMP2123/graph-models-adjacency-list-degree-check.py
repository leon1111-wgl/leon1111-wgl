# Leon | Original learning example
# Build an undirected adjacency list
# Python 3.12+ | Run: python graph-models-adjacency-list-degree-check.py
vertices = ["A", "B", "C", "D", "E"]
edges = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D")]
graph = {vertex: [] for vertex in vertices}
for u, v in edges:
    graph[u].append(v)
    graph[v].append(u)
for vertex in vertices:
    print(vertex, graph[vertex])
print("degree sum:", sum(len(graph[v]) for v in vertices))
print("twice edges:", 2 * len(edges))
