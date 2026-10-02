# Guoliang | Original learning example
# Measure two proposed boxes
# Python 3.12+ | Run: python detection-overlap-box-overlap.py
a = (0, 0, 4, 4)
b = (1, 1, 5, 5)
width = max(0, min(a[2], b[2]) - max(a[0], b[0]))
height = max(0, min(a[3], b[3]) - max(a[1], b[1]))
intersection = width * height
area_a = (a[2] - a[0]) * (a[3] - a[1])
area_b = (b[2] - b[0]) * (b[3] - b[1])
iou = intersection / (area_a + area_b - intersection)
print(f"intersection={intersection}; IoU={iou:.4f}")
for threshold in [0.3, 0.5]:
    print(threshold, "suppress B" if iou > threshold else "keep B")
