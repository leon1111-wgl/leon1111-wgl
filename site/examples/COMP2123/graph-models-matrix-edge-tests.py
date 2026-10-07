# Leon | Original learning example
# Trade matrix space for direct edge tests
# Python 3.12+ | Run: python graph-models-matrix-edge-tests.py
vertices = ["A", "B", "C"]
index = {v: i for i, v in enumerate(vertices)}
matrix = [[False] * 3 for _ in vertices]
for u, v in [("A", "B"), ("B", "C")]:
    matrix[index[u]][index[v]] = True
print("A to B:", matrix[index["A"]][index["B"]])
print("B to A:", matrix[index["B"]][index["A"]])
neighbors = [vertices[j] for j in range(3) if matrix[index["B"]][j]]
print("B neighbors:", neighbors)
print("cells:", sum(len(row) for row in matrix))
