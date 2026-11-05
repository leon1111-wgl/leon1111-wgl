"""Choose the threshold with the lowest validation cost and save it.  Usage: python3 choose_threshold.py"""
import json
from pathlib import Path

import numpy as np

from fraud import MISSED_COST, REVIEW_COST, cost, cost_curve, fit, scores, splits

(X_train, y_train), (X_val, y_val), _test_stays_closed = splits()
score = scores(fit(X_train, y_train), X_val)

grid = np.round(np.arange(0.01, 0.6001, 0.005), 3)
costs = cost_curve(y_val, score, grid)
best = grid[costs.argmin()]
plateau = grid[costs <= costs.min() * 1.03]
chosen = float(np.round(np.median(plateau), 3))

print(f"costs: {REVIEW_COST:g} per flagged payment, {MISSED_COST:g} per fraud not flagged")
print(f"if the scores were true probabilities, flag when p > {REVIEW_COST:g}/{MISSED_COST:g} = {REVIEW_COST / MISSED_COST:.3f}")
print(f"{'threshold':>9} {'flagged':>8} {'cost':>8}")
for t in (0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.08, 0.10, 0.20, 0.50):
    flagged = score >= t
    print(f"{t:>9.2f} {flagged.sum():>8} {cost(y_val, flagged):>8,.0f}")
print(f"lowest cost at {best}; thresholds within 3% of that cost run from {plateau.min()} to {plateau.max()}")
print(f"chosen threshold, the middle of that range: {chosen}")

Path("threshold.json").write_text(json.dumps(
    {"threshold": chosen, "review_cost": REVIEW_COST, "missed_cost": MISSED_COST,
     "chosen_on": "validation", "model": "logistic regression, no class weights"}, indent=1))
print("saved threshold.json")
