# Leon | Original learning example
# Order tasks by reversed DFS finishing times
# Python 3.12+ | Run: python topological-scc-topo-dfs-finishing.py
def topological_order(graph):
    """Return the vertices in a valid order, or None if a directed cycle exists."""
    state = {v: "new" for v in graph}       # new -> active -> done
    finished = []                           # vertices in the order they finish

    def visit(u):
        state[u] = "active"                 # u is on the current DFS path
        for v in graph[u]:
            if state[v] == "active":
                return False                # edge back to the path: a cycle
            if state[v] == "new" and not visit(v):
                return False
        state[u] = "done"
        finished.append(u)
        return True

    for u in graph:
        if state[u] == "new" and not visit(u):
            return None
    print("finishing order:", finished)
    return finished[::-1]                   # latest finisher goes first

meals = {
    "shop": ["chop", "boil"],
    "chop": ["fry"],
    "boil": ["pasta"],
    "fry": ["mix"],
    "pasta": ["mix"],
    "mix": ["serve"],
    "serve": [],
}
print("order:", topological_order(meals))

stuck = {"plan": ["unlock"], "unlock": ["enter"], "enter": ["key"], "key": ["unlock"]}
print("order:", topological_order(stuck))
