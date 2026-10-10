# Leon | Original learning example
# Start BFS from every exit at once
# Python 3.12+ | Run: python bfs-distance-nearest-exit-wavefront.py
from collections import deque

def nearest_exit(grid, exits):
    rows, cols = len(grid), len(grid[0])
    if any(len(row) != cols for row in grid):
        raise ValueError("rectangular grid required")
    distance = {}
    queue = deque()
    for r, c in exits:
        if not (0 <= r < rows and 0 <= c < cols) or grid[r][c] == "#":
            raise ValueError("exit must be an open cell")
        if (r, c) not in distance:
            distance[r, c] = 0
            queue.append((r, c))
    while queue:
        r, c = queue.popleft()
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = r + dr, c + dc
            if (0 <= nr < rows and 0 <= nc < cols and
                    grid[nr][nc] != "#" and (nr, nc) not in distance):
                distance[nr, nc] = distance[r, c] + 1
                queue.append((nr, nc))
    return distance

grid = ["..#.", "....", ".#.."]
distance = nearest_exit(grid, [(0, 0), (2, 3)])
assert distance[0, 3] == 2 and distance[1, 1] == 2
assert nearest_exit(grid, []) == {}
for r, row in enumerate(grid):
    print(" ".join("#" if cell == "#" else str(distance.get((r, c), "X"))
                   for c, cell in enumerate(row)))
