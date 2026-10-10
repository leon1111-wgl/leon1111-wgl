# Leon | Original learning example
# Compute a finite loss even when a probability underflows
# Python 3.12+ | Run: python dl-softmax-loss-stable-loss-gradient-check.py
from math import exp, log, isclose

def probabilities(logits):
    peak = max(logits)
    weights = [exp(z - peak) for z in logits]
    return [w / sum(weights) for w in weights]

def cross_entropy(logits, target):
    peak = max(logits)
    return (peak - logits[target]) + log(sum(exp(z - peak) for z in logits))

logits = [1000.0, 0.0, -1000.0]
target = 2
p = probabilities(logits)
loss = cross_entropy(logits, target)
gradient = [value - int(j == target) for j, value in enumerate(p)]
epsilon = 1e-4
numeric = []
for j in range(len(logits)):
    plus, minus = logits.copy(), logits.copy()
    plus[j] += epsilon
    minus[j] -= epsilon
    numeric.append((cross_entropy(plus, target) - cross_entropy(minus, target)) / (2 * epsilon))
assert p[target] == 0.0 and loss == 2000.0
assert all(isclose(a, b, abs_tol=1e-6) for a, b in zip(gradient, numeric))
print("target probability:", p[target])
print(f"finite loss: {loss:.1f}")
print("analytic gradient:", gradient)
print("numeric gradient:", [round(value, 6) for value in numeric])
