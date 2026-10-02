# Guoliang | Original learning example
# Matrices: several examples at once
# Python 3.12+ | Run: python matrices-shapes-first-steps.py
rows = [[1, 2], [3, 4]]
weights = [2, -1]
scores = []
for row in rows:
    assert len(row) == len(weights)
    score = 0
    for column in range(len(weights)):
        score = score + row[column] * weights[column]
    scores.append(score)
print("shape:", len(rows), "by", len(weights))
print("scores:", scores)
