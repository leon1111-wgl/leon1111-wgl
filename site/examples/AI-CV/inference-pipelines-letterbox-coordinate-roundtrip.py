# Leon | Original learning example
# Return a detection box to the original image
# Python 3.12+ | Run: python inference-pipelines-letterbox-coordinate-roundtrip.py
from math import isclose

def metadata(width, height, side):
    if min(width, height, side) <= 0:
        raise ValueError("positive dimensions required")
    nominal = min(side / width, side / height)
    rw, rh = max(1, round(width * nominal)), max(1, round(height * nominal))
    return rw / width, rh / height, (side - rw) // 2, (side - rh) // 2

def forward(box, meta):
    sx, sy, px, py = meta
    x1, y1, x2, y2 = box
    return [sx * x1 + px, sy * y1 + py, sx * x2 + px, sy * y2 + py]

def restore(box, meta, width, height):
    sx, sy, px, py = meta
    x1, y1, x2, y2 = box
    restored = [(x1 - px) / sx, (y1 - py) / sy,
                (x2 - px) / sx, (y2 - py) / sy]
    clipped = [min(max(v, 0.0), limit)
               for v, limit in zip(restored, [width, height, width, height])]
    return clipped if clipped[0] < clipped[2] and clipped[1] < clipped[3] else None

original = [100.0, 50.0, 500.0, 300.0]
meta = metadata(800, 400, 640)
model_box = forward(original, meta)
restored = restore(model_box, meta, 800, 400)
assert all(isclose(a, b) for a, b in zip(original, restored))
odd_meta = metadata(853, 480, 640)
odd_back = restore(forward(original, odd_meta), odd_meta, 853, 480)
assert all(isclose(a, b) for a, b in zip(original, odd_back))
assert odd_meta[0] != odd_meta[1]  # Rounded height changes the actual y scale.
assert restore([0, 0, 20, 20], meta, 800, 400) is None
print("scale and padding:", meta)
print("model box:", model_box)
print("original box:", restored)
print("rounded-size round trip:", all(isclose(a, b) for a, b in zip(original, odd_back)))
