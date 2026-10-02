# Guoliang | Original learning example
# Find and average two neighbors
# Python 3.12+ | Run: python learning-neighbors-nearest-two-trace.py
records = [(0, 2), (4, 10), (7, 16)]
query = 5
ranked = []
for x, target in records:
    distance = abs(x - query)
    ranked.append((distance, x, target))
ranked.sort()
selected = ranked[:2]
total = 0
for distance, x, target in selected:
    total += target
prediction = total / len(selected)
print("Neighbors:", selected)
print("Prediction:", prediction)
assert prediction == 13
