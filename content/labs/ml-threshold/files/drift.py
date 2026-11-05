"""Two reasons the chosen threshold will not stay put.  Usage: python3 drift.py"""
import json
from pathlib import Path

import numpy as np

from fraud import (
    REVIEW_COST,
    cost,
    cost_curve,
    fit,
    make_payments,
    scores,
    splits,
)

frozen = json.loads(Path("threshold.json").read_text())["threshold"]
(X_train, y_train), (X_val, y_val), _test_stays_closed = splits()
model = fit(X_train, y_train)
grid = np.round(np.arange(0.01, 0.6001, 0.005), 3)

# 1. Sampling noise: re-draw the validation set with replacement and ask for the best threshold each time.
score_val = scores(model, X_val)
rs = np.random.RandomState(3)
best_each = []
for _ in range(200):
    pick = rs.randint(0, len(y_val), len(y_val))
    best_each.append(grid[cost_curve(y_val[pick], score_val[pick], grid).argmin()])
p10, p50, p90 = np.percentile(best_each, [10, 50, 90])
print(f"1. best threshold on 200 re-drawn validation sets: 10th {p10:.3f}, median {p50:.3f}, 90th {p90:.3f}")
print(f"   (the saved threshold is {frozen}; the validation set has {int(y_val.sum())} fraud cases)\n")

# 2. Change: what the saved threshold costs when the world moves.
X_later, y_later = make_payments(6000, seed=21, shift=0.8)
scenarios = [
    ("validation, as chosen", y_val, score_val, REVIEW_COST),
    ("later month, fraud more common", y_later, scores(model, X_later), REVIEW_COST),
    ("validation, analyst time 5 -> 12", y_val, score_val, 12.0),
]
print(f"2. saved threshold {frozen} against the best threshold for each situation")
print(f"{'situation':<34} {'fraud rate':>10} {'best t':>7} {'cost at saved t':>16} {'cost at best t':>15} {'extra':>7}")
for name, y, score, review in scenarios:
    costs = cost_curve(y, score, grid, review=review)
    here = cost(y, score >= frozen, review=review)
    print(f"{name:<34} {y.mean():>10.3f} {grid[costs.argmin()]:>7.3f} {here:>16,.0f} {costs.min():>15,.0f} {here / costs.min() - 1:>7.1%}")
