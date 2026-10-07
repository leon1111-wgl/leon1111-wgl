# Leon | Original learning example
# Trace two Lloyd steps
# Python 3.12+ | Run: python kmeans-lloyd-two-clusters.py
points = [1, 3, 9, 11]
centers = [1, 9]
for step in range(2):
    groups = [[], []]
    for point in points:
        distances = [abs(point - centers[0]), abs(point - centers[1])]
        group_id = 0 if distances[0] <= distances[1] else 1
        groups[group_id].append(point)
    centers = [sum(group) / len(group) for group in groups]
    error = 0
    for group_id, group in enumerate(groups):
        for point in group:
            error += (point - centers[group_id]) ** 2
    print(f"Step {step + 1}: centers={centers}, SSE={error:.1f}")
assert centers == [2.0, 10.0]
