# Guoliang | Original learning example
# Remove an isolated speck
# Python 3.12+ | Run: python edges-morphology-binary-opening.py
mask = [0, 1, 0, 0, 1, 1, 1, 0]
def local_rule(values, operation):
    padded = [0] + values + [0]
    return [operation(padded[i:i + 3]) for i in range(len(values))]
eroded = local_rule(mask, min)
opened = local_rule(eroded, max)
print("eroded:", eroded)
print("opened:", opened)
