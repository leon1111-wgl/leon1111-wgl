"""Do predicted probabilities match what happened?  Plain model against class_weight='balanced'."""
from itertools import pairwise

import numpy as np
from sklearn.metrics import brier_score_loss, roc_auc_score

from fraud import MISSED_COST, REVIEW_COST, cost_curve, fit, scores, splits

(X_train, y_train), (X_val, y_val), _test_stays_closed = splits()
grid = np.round(np.arange(0.01, 0.9901, 0.005), 3)
edges = [0.0, 0.02, 0.05, 0.10, 0.20, 0.40, 1.0001]

for balanced in (False, True):
    score = scores(fit(X_train, y_train, balanced), X_val)
    print(f"model: {'class_weight=balanced' if balanced else 'no class weights'}")
    print(f"  ROC AUC {roc_auc_score(y_val, score):.3f}   Brier score {brier_score_loss(y_val, score):.4f}   (lower Brier is better)")
    print(f"  {'score range':<12} {'payments':>8} {'mean score':>11} {'fraud rate':>11}")
    for low, high in pairwise(edges):
        inside = (score >= low) & (score < high)
        if inside.sum():
            print(f"  {low:.2f}-{min(high, 1):.2f}    {inside.sum():>8} {score[inside].mean():>11.3f} {y_val[inside].mean():>11.3f}")
    costs = cost_curve(y_val, score, grid)
    best = grid[costs.argmin()]
    print(f"  lowest validation cost {costs.min():,.0f} at threshold {best} "
          f"(calibrated scores would give about {REVIEW_COST / MISSED_COST:.2f})\n")
