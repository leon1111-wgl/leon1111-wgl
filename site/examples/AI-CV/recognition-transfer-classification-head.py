# Guoliang | Original learning example
# Turn features into three scores
# Python 3.12+ | Run: python recognition-transfer-classification-head.py
import math
features = [1, 2]
weights = [[1, 0], [0, 1], [0, 0]]
scores = [sum(w * h for w, h in zip(row, features)) for row in weights]
exp_scores = [math.exp(s - max(scores)) for s in scores]
probabilities = [v / sum(exp_scores) for v in exp_scores]
print("scores:", scores)
print("probabilities:", [round(p, 4) for p in probabilities])
print(f"loss={-math.log(probabilities[1]):.4f}")
