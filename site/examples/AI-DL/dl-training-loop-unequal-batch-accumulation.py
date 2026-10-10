# Leon | Original learning example
# Accumulate gradients when microbatches have different sizes
# Python 3.12+ | Run: python dl-training-loop-unequal-batch-accumulation.py
from math import isclose
x = [1.0, 2.0, 3.0, 4.0]
y = [2.0 * value for value in x]
weight = 0.0

def mean_gradient(indices, weight):
    return sum(2 * (weight * x[i] - y[i]) * x[i] for i in indices) / len(indices)

batches = [[0, 1, 2], [3]]
batch_gradients = [mean_gradient(batch, weight) for batch in batches]
wrong = sum(batch_gradients) / len(batches)
accumulated = sum(len(batch) * gradient for batch, gradient in zip(batches, batch_gradients)) / len(x)
full = mean_gradient(list(range(len(x))), weight)
updated = weight - 0.01 * accumulated
assert isclose(full, -30.0) and isclose(accumulated, full)
assert not isclose(wrong, full) and isclose(updated, 0.3)
print("batch gradients:", [round(g, 6) for g in batch_gradients])
print(f"unweighted mean: {wrong:.6f}")
print(f"sample-weighted gradient: {accumulated:.6f}")
print(f"one optimizer step: {updated:.6f}")
