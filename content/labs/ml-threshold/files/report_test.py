"""Report on the test set with the saved threshold.  Usage: python3 report_test.py"""
import json
from pathlib import Path

import numpy as np
from sklearn.metrics import confusion_matrix

from fraud import cost, fit, scores, splits

config = json.loads(Path("threshold.json").read_text())
threshold = config["threshold"]
(X_train, y_train), _validation, (X_test, y_test) = splits()
score = scores(fit(X_train, y_train), X_test)
n = len(y_test)
flagged = score >= threshold

tn, fp, fn, tp = confusion_matrix(y_test, flagged).ravel()
print(f"test: {n} payments, {y_test.sum()} fraud. Threshold {threshold} was chosen on validation and not touched here.")
print("                 predicted ok   predicted fraud")
print(f"actual ok        {tn:>12}   {fp:>15}")
print(f"actual fraud     {fn:>12}   {tp:>15}")

print(f"\n{'policy':<26} {'flagged/1000':>12} {'cost/1000':>10}")
for name, mask in [("flag nothing", np.zeros(n, bool)), ("default threshold 0.5", score >= 0.5),
                   (f"chosen threshold {threshold}", flagged), ("flag everything", np.ones(n, bool))]:
    print(f"{name:<26} {mask.sum() / n * 1000:>12.0f} {cost(y_test, mask) / n * 1000:>10,.0f}")

rs = np.random.RandomState(5)
caught = (flagged[y_test == 1]).astype(float)
recalls = [rs.choice(caught, len(caught)).mean() for _ in range(1000)]
low, high = np.percentile(recalls, [5, 95])
print(f"\nrecall {tp / (tp + fn):.2f}, with a 90% bootstrap interval of {low:.2f} to {high:.2f} ({int(y_test.sum())} fraud cases)")
