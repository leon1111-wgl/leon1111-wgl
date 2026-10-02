# Guoliang | Original learning example
# Compare two possible responses
# Python 3.12+ | Run: python conditional-generation-response-probability.py
import math
correct = [0.4, 0.5, 0.9]
incorrect = [0.5, 0.7, 0.9]
probability = math.prod(correct)
mean_loss = -sum(math.log(p) for p in correct) / len(correct)
print(f"correct probability={probability:.3f}")
print(f"incorrect probability={math.prod(incorrect):.3f}")
print(f"mean loss={mean_loss:.4f}")
