# Guoliang | Original learning example
# Powers and logarithms without mystery
# Python 3.12+ | Run: python powers-logarithms-first-steps.py
import math
print("power:", 2 ** 3)
print("reverse:", math.log2(8))
for probability in [0.8, 0.2, 1.0]:
    loss = -math.log(probability)
    print(f"p={probability:.1f}, loss={loss:.4f}")
