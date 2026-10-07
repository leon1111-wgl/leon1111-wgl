# Leon | Original learning example
# Combine only available evidence
# Python 3.12+ | Run: python early-late-fusion-weighted-fusion.py
scores = {"image": 0.8, "audio": 0.4}
weights = {"image": 0.75, "audio": 0.25}
def fuse(available):
    total = sum(weights[name] for name in available)
    return sum(weights[name] * score for name, score in available.items()) / total
print(f"both={fuse(scores):.2f}")
print(f"image only={fuse({'image': 0.8}):.2f}")
print("early feature list:", [0.2, 0.9] + [0.6, 0.1])
