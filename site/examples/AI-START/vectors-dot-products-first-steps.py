# Leon | Original learning example
# Vectors and the dot product
# Python 3.12+ | Run: python vectors-dot-products-first-steps.py
features = [3, 4]
weights = [2, -1]
assert len(features) == len(weights)
score = 0
for position in range(len(features)):
    contribution = features[position] * weights[position]
    score = score + contribution
    print("contribution:", contribution)
print("score:", score)
