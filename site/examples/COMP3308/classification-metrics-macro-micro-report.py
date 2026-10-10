# Leon | Original learning example
# See which class disappears inside an average
# Python 3.12+ | Run: python classification-metrics-macro-micro-report.py
from math import isclose
labels = ["leaf", "flower", "seed"]
truth = ["leaf"] * 8 + ["flower", "seed"]
predicted = ["leaf"] * 9 + ["seed"]

def report(truth, predicted, labels):
    if len(truth) != len(predicted) or not truth:
        raise ValueError("nonempty aligned observations required")
    if set(truth + predicted) - set(labels):
        raise ValueError("unknown label")
    per_class = []
    total_tp = total_fp = total_fn = 0
    for label in labels:
        tp = sum(t == label and p == label for t, p in zip(truth, predicted))
        fp = sum(t != label and p == label for t, p in zip(truth, predicted))
        fn = sum(t == label and p != label for t, p in zip(truth, predicted))
        denominator = 2 * tp + fp + fn
        f1 = 2 * tp / denominator if denominator else 0.0
        per_class.append((label, tp, fp, fn, f1))
        total_tp += tp; total_fp += fp; total_fn += fn
    macro = sum(row[4] for row in per_class) / len(labels)
    micro = 2 * total_tp / (2 * total_tp + total_fp + total_fn)
    return per_class, macro, micro

rows, macro, micro = report(truth, predicted, labels)
for label, tp, fp, fn, f1 in rows:
    print(f"{label}: TP={tp} FP={fp} FN={fn} F1={f1:.4f}")
accuracy = sum(t == p for t, p in zip(truth, predicted)) / len(truth)
assert isclose(macro, (16/17 + 0 + 1)/3) and isclose(micro, accuracy)
print(f"macro F1={macro:.4f}; micro F1={micro:.4f}; accuracy={accuracy:.4f}")
