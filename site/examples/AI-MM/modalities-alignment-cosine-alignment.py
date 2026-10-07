# Leon | Original learning example
# Compare two descriptions
# Python 3.12+ | Run: python modalities-alignment-cosine-alignment.py
import math
def unit(values):
    length = math.sqrt(sum(x * x for x in values))
    if length == 0:
        raise ValueError("A zero vector has no direction")
    return [x / length for x in values]
image = unit([3, 4])
for name, values in [("A", [0, 2]), ("B", [2, 0])]:
    text = unit(values)
    similarity = sum(a * b for a, b in zip(image, text))
    print(f"{name}: {similarity:.2f}")
