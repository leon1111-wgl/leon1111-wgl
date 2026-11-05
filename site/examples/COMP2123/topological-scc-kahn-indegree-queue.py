# Leon | Original learning example
# Order tasks with in-degrees and a queue
# Python 3.12+ | Run: python topological-scc-kahn-indegree-queue.py
from collections import deque

def kahn(graph):
    indegree = {v: 0 for v in graph}
    for u in graph:
        for v in graph[u]:
            indegree[v] += 1                # count the edges that enter v
    ready = deque(v for v in graph if indegree[v] == 0)
    order = []
    while ready:
        u = ready.popleft()
        order.append(u)
        for v in graph[u]:
            indegree[v] -= 1                # u is placed, so one prerequisite is met
            if indegree[v] == 0:
                ready.append(v)
    return order

meals = {
    "shop": ["chop", "boil"],
    "chop": ["fry"],
    "boil": ["pasta"],
    "fry": ["mix"],
    "pasta": ["mix"],
    "mix": ["serve"],
    "serve": [],
}
order = kahn(meals)
print("order:", order)
position = {v: i for i, v in enumerate(order)}
print("all edges point forward:", all(position[u] < position[v] for u in meals for v in meals[u]))

stuck = {"plan": ["unlock"], "unlock": ["enter"], "enter": ["key"],
         "key": ["unlock"], "party": []}
order = kahn(stuck)
print("placed:", order)
print("blocked:", [v for v in stuck if v not in order])
