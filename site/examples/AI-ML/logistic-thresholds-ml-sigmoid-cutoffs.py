# Guoliang | Original learning example
# One probability, two decisions
# Python 3.12+ | Run: python logistic-thresholds-ml-sigmoid-cutoffs.py
from math import exp
x, w, b = 2., 0.8, -1.2
score = b + w * x
probability = 1 / (1 + exp(-score))
print(f'score: {score:.4f}; probability: {probability:.4f}')
for threshold in [0.50, 0.65]:
    label = int(probability >= threshold)
    print(f'threshold {threshold:.2f}: class {label}')
