# Leon | Original learning example
# Measure the curse of dimensionality
# Python 3.12+ | Run: python knn-practice-curse-of-dimensionality-numbers.py
import math
import random

# 1. How much room does a neighbourhood need? (uniform data in the unit cube)
print("dims  edge holding 1% of the cube  points for 10 per axis  nearest/farthest")
rng = random.Random(11)


def nearest_over_farthest(dims, points=100, queries=30):
    total = 0.0
    for _ in range(queries):
        data = [[rng.random() for _ in range(dims)] for _ in range(points)]
        query = [rng.random() for _ in range(dims)]
        gaps = [math.dist(row, query) for row in data]
        total += min(gaps) / max(gaps)
    return total / queries


for dims in (1, 2, 10, 100, 1000):
    edge = 0.01 ** (1 / dims)
    print(f"{dims:>4}  {edge:>27.3f}  {'10^' + str(dims):>21}  {nearest_over_farthest(dims):>16.3f}")


# 2. Add useless columns to a problem that two columns solve.
def make_data(extra, seed, per_class=30):
    rand = random.Random(seed)
    rows = []
    for label, centre in enumerate((0.3, 0.7)):
        for _ in range(per_class):
            useful = [centre + (rand.random() - 0.5) * 0.3 for _ in range(2)]
            rows.append((useful + [rand.random() for _ in range(extra)], label))
    return rows


def leave_one_out_accuracy(rows):
    right = 0
    for i, (x, label) in enumerate(rows):
        others = [(math.dist(x, z), other) for j, (z, other) in enumerate(rows) if j != i]
        right += min(others)[1] == label
    return right / len(rows)


print("useless columns  1-NN accuracy (mean of 5 data sets)")
for extra in (0, 2, 10, 50, 200):
    scores = [leave_one_out_accuracy(make_data(extra, seed)) for seed in range(5)]
    print(f"{extra:>15}  {sum(scores) / len(scores):.3f}")
