"""Burn-in failure model: report a cross-validated ROC AUC for the go/no-go review.

Usage: python3 train.py [--shuffle-labels]
"""
import argparse

import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import RepeatedStratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler

from sensors import Plant

K = 10
CV = RepeatedStratifiedKFold(n_splits=5, n_repeats=3, random_state=0)


def prepare(X, y):
    """Put the sensors on one scale and keep the K columns most related to the label."""
    X = StandardScaler().fit_transform(X)
    return SelectKBest(f_classif, k=K).fit_transform(X, y)


def cv_estimate(X, y):
    Xp = prepare(X, y)
    scores = cross_val_score(LogisticRegression(max_iter=1000), Xp, y, cv=CV, scoring="roc_auc")
    return scores.mean(), scores.std()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--shuffle-labels", action="store_true",
                        help="control: average over 5 random relabelings, so no real signal remains")
    args = parser.parse_args()

    X, y = Plant().batch(150, seed=1)
    print(f"{X.shape[0]} units, {X.shape[1]} sensors, {int(y.sum())} failures")
    if args.shuffle_labels:
        means = [cv_estimate(X, np.random.RandomState(s).permutation(y))[0] for s in range(5)]
        print(f"control, labels shuffled: mean ROC AUC {np.mean(means):.3f} over 5 shuffles")
    else:
        mean, std = cv_estimate(X, y)
        print(f"cross-validated ROC AUC: {mean:.3f} (std {std:.3f} over 15 folds)")


if __name__ == "__main__":
    main()
