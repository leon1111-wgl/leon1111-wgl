"""Compare where the preprocessing happens relative to the cross-validation split.

Usage: python3 compare.py [--shuffle-labels | --fresh]
  (no flag)         the four variants on the real labels
  --shuffle-labels  the same four variants with the labels shuffled, so no real signal remains
  --fresh           the cross-validated estimate against a brand-new batch of units
"""
import argparse

import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import RepeatedStratifiedKFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from sensors import Plant

K = 10
CV = RepeatedStratifiedKFold(n_splits=5, n_repeats=3, random_state=0)


def classifier():
    return LogisticRegression(max_iter=1000)


def selector():
    return SelectKBest(f_classif, k=K)


def auc(model, X, y):
    return cross_val_score(model, X, y, cv=CV, scoring="roc_auc").mean()


def scaler_first(X, y):
    """Leak: the scaler has seen every row, including the ones held out in each fold."""
    return auc(make_pipeline(selector(), classifier()), StandardScaler().fit_transform(X), y)


def selector_first(X, y):
    """Leak: the selector has seen every label, including the ones held out in each fold."""
    return auc(make_pipeline(StandardScaler(), classifier()), selector().fit_transform(X, y), y)


def both_first(X, y):
    """What train.py does."""
    return auc(classifier(), selector().fit_transform(StandardScaler().fit_transform(X), y), y)


def pipeline(X, y):
    """Every step is refitted on the training part of each fold only."""
    return auc(make_pipeline(StandardScaler(), selector(), classifier()), X, y)


VARIANTS = [
    ("scaler fitted on all rows, then CV", scaler_first),
    ("selector fitted on all rows, then CV", selector_first),
    ("both fitted on all rows, then CV", both_first),
    ("both inside a Pipeline", pipeline),
]


def table(X, y, shuffles):
    print(f"{'variant':<40} {'ROC AUC':>8}")
    for name, fn in VARIANTS:
        if shuffles:
            score = np.mean([fn(X, np.random.RandomState(s).permutation(y)) for s in range(shuffles)])
        else:
            score = fn(X, y)
        print(f"{name:<40} {score:>8.3f}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--shuffle-labels", action="store_true")
    parser.add_argument("--fresh", action="store_true")
    args = parser.parse_args()

    plant = Plant()
    X, y = plant.batch(150, seed=1)
    if args.fresh:
        X_new, y_new = plant.batch(3000, seed=2)
        final = make_pipeline(StandardScaler(), selector(), classifier()).fit(X, y)
        print(f"{'estimate from CV, both fitted first':<40} {both_first(X, y):>8.3f}")
        print(f"{'estimate from CV, Pipeline':<40} {pipeline(X, y):>8.3f}")
        print(f"{'deployed model on 3000 new units':<40} {roc_auc_score(y_new, final.predict_proba(X_new)[:, 1]):>8.3f}")
    elif args.shuffle_labels:
        print("labels shuffled, mean over 5 shuffles (the true answer is chance):")
        table(X, y, shuffles=5)
    else:
        print(f"{X.shape[0]} units, {X.shape[1]} sensors, {int(y.sum())} failures")
        table(X, y, shuffles=0)


if __name__ == "__main__":
    main()
