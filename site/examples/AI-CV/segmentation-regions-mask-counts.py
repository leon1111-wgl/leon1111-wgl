# Guoliang | Original learning example
# Count foreground overlap
# Python 3.12+ | Run: python segmentation-regions-mask-counts.py
prediction = [1, 1, 1, 0, 0, 0]
reference = [0, 1, 1, 1, 0, 0]
shared = sum(p == 1 and g == 1 for p, g in zip(prediction, reference))
union = sum(p == 1 or g == 1 for p, g in zip(prediction, reference))
iou = shared / union
dice = 2 * shared / (sum(prediction) + sum(reference))
print("shared:", shared, "union:", union)
print(f"IoU={iou:.4f}; Dice={dice:.4f}")
