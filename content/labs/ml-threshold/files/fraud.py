"""Fabricated card payments and the cost rule the review team works under.

Every number is invented. Costs are per payment, in the same made-up currency.
"""
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

REVIEW_COST = 5.0     # analyst time spent on every payment we flag, fraud or not
MISSED_COST = 100.0   # average loss when a fraud payment is not flagged


def make_payments(n, seed, shift=0.0):
    """n payments. `shift` raises the log-odds of fraud for everyone, i.e. fraud became more common."""
    rs = np.random.RandomState(seed)
    log_amount = rs.normal(3.6, 1.0, n)
    night = (rs.rand(n) < 0.18).astype(float)
    new_device = (rs.rand(n) < 0.12).astype(float)
    mismatch = (rs.rand(n) < 0.07).astype(float)
    txns_24h = rs.poisson(2.0, n).astype(float)
    log_age = rs.normal(5.5, 1.2, n)
    logit = (-5.2 + 0.8 * (log_amount - 3.6) + 1.4 * night + 1.8 * new_device
             + 2.0 * mismatch + 0.3 * txns_24h - 0.5 * (log_age - 5.5) + shift)
    fraud = (rs.rand(n) < 1 / (1 + np.exp(-logit))).astype(int)
    X = np.column_stack([log_amount, night, new_device, mismatch, txns_24h, log_age])
    return X, fraud


def splits():
    """One month of 12,000 payments cut into train, validation and test, in that order."""
    X, y = make_payments(12000, seed=11)
    return (X[:6000], y[:6000]), (X[6000:9000], y[6000:9000]), (X[9000:], y[9000:])


def fit(X, y, balanced=False):
    weight = "balanced" if balanced else None
    return make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, class_weight=weight)).fit(X, y)


def scores(model, X):
    return model.predict_proba(X)[:, 1]


def cost(y, flagged, review=REVIEW_COST, missed=MISSED_COST):
    """Total cost: every flagged payment is reviewed, every fraud we did not flag is lost."""
    flagged = np.asarray(flagged, dtype=bool)
    return review * flagged.sum() + missed * ((y == 1) & ~flagged).sum()


def cost_curve(y, score, grid, review=REVIEW_COST, missed=MISSED_COST):
    return np.array([cost(y, score >= t, review, missed) for t in grid])
