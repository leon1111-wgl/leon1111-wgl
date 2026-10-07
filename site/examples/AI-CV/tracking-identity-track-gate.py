# Leon | Original learning example
# Predict and gate one track
# Python 3.12+ | Run: python tracking-identity-track-gate.py
previous, current = 2, 5
velocity = current - previous
predicted = current + velocity
detections = [8, 15]
nearest = min(detections, key=lambda x: abs(x - predicted))
accepted = abs(nearest - predicted) <= 2
print("predicted:", predicted)
print("nearest:", nearest, "accepted:", accepted)
