# Leon | Original learning example
# Slopes, gradients and one learning step
# Python 3.12+ | Run: python slopes-gradients-first-steps.py
def loss(weight):
    return (weight - 3) ** 2

weight = 0.0
step = 0.001
approx_slope = (loss(weight + step) - loss(weight - step)) / (2 * step)
slope = 2 * (weight - 3)
new_weight = weight - 0.1 * slope
print(f"estimated slope: {approx_slope:.3f}")
print(f"before: w={weight:.2f}, loss={loss(weight):.2f}")
print(f"after: w={new_weight:.2f}, loss={loss(new_weight):.2f}")
assert loss(new_weight) < loss(weight)
