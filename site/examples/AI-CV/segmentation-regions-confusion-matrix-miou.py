# Leon | Original learning example
# Compute segmentation IoU without counting ignored pixels
# Python 3.12+ | Run: python segmentation-regions-confusion-matrix-miou.py
from math import isclose

def segmentation_report(truth, prediction, classes, ignore=255):
    if len(truth) != len(prediction) or classes <= 0:
        raise ValueError("aligned arrays and positive class count required")
    matrix = [[0] * classes for _ in range(classes)]
    for actual, predicted in zip(truth, prediction):
        if actual == ignore:
            continue
        if not (0 <= actual < classes and 0 <= predicted < classes):
            raise ValueError("unknown class")
        matrix[actual][predicted] += 1
    ious = []
    for c in range(classes):
        tp = matrix[c][c]
        actual_total = sum(matrix[c])
        predicted_total = sum(row[c] for row in matrix)
        union = actual_total + predicted_total - tp
        ious.append(tp / union if union else None)
    defined = [value for value in ious if value is not None]
    mean = sum(defined) / len(defined) if defined else None
    total = sum(map(sum, matrix))
    accuracy = sum(matrix[c][c] for c in range(classes)) / total if total else None
    return matrix, ious, mean, accuracy

truth = [0, 0, 0, 1, 1, 2, 2, 255]
prediction = [0, 0, 1, 1, 2, 2, 0, 1]
matrix, ious, mean, accuracy = segmentation_report(truth, prediction, 3)
assert matrix == [[2, 1, 0], [0, 1, 1], [1, 0, 1]]
assert isclose(mean, 7 / 18) and isclose(accuracy, 4 / 7)
assert segmentation_report([255], [1], 3)[2] is None
assert segmentation_report([0], [0], 3)[1] == [1.0, None, None]
print("rows = truth; columns = prediction:")
for row in matrix:
    print(row)
print("class IoU:", [round(value, 6) for value in ious])
print(f"mean IoU: {mean:.6f}")
print(f"pixel accuracy: {accuracy:.6f}")
