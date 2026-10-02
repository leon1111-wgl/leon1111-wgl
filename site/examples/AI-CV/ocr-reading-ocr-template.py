# Guoliang | Original learning example
# Count symbol mismatches
# Python 3.12+ | Run: python ocr-reading-ocr-template.py
templates = {"H": [1, 0, 1, 1, 1, 0, 1], "I": [0, 1, 0, 1, 0, 1, 0]}
observed = [1, 0, 1, 1, 1, 0, 0]
distances = {}
for label, template in templates.items():
    distances[label] = sum(a != b for a, b in zip(observed, template))
print("distances:", distances)
print("closest:", min(distances, key=distances.get))
