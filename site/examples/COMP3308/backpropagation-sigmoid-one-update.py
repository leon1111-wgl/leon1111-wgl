# Guoliang | Original learning example
# Check one sigmoid update
# Python 3.12+ | Run: python backpropagation-sigmoid-one-update.py
import math

x, target = 2.0, 1.0
weight, bias = 0.0, 0.0
rate = 0.1
score = weight * x + bias
activation = 1 / (1 + math.exp(-score))
delta = (activation - target) * activation * (1 - activation)
weight_gradient = delta * x
bias_gradient = delta
weight = weight - rate * weight_gradient
bias = bias - rate * bias_gradient
print(f"Old output: {activation:.6f}")
print(f"New weight: {weight:.6f}")
print(f"New bias: {bias:.6f}")
print(f"New score: {weight * x + bias:.6f}")
assert abs(weight - 0.025) < 1e-12
