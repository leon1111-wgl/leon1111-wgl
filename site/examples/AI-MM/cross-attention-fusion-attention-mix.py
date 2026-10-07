# Leon | Original learning example
# Let a query mix two values
# Python 3.12+ | Run: python cross-attention-fusion-attention-mix.py
import math
query = [1, 0]
keys = [[2, 0], [0, 2]]
values = [[10, 0], [0, 4]]
scores = [sum(q * k for q, k in zip(query, key)) / math.sqrt(2) for key in keys]
weights = [math.exp(s - max(scores)) for s in scores]
weights = [w / sum(weights) for w in weights]
output = [sum(weight * value[j] for weight, value in zip(weights, values)) for j in range(2)]
print("weights:", [round(w, 4) for w in weights])
print("output:", [round(x, 4) for x in output])
