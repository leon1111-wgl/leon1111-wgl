"""Compare later windows with the training window.

Usage: python3 monitor.py            inputs and predictions only (labels have not arrived yet)
       python3 monitor.py --labels   as above, plus the late rate once the labels are in
       python3 monitor.py --noise    how much PSI moves when nothing changed
"""
import argparse

import numpy as np
from scipy.stats import ks_2samp

from policy import decide
from world import FEATURES, design, fit_reference, later_windows, make_window

RELIANCE_FLOOR = 0.05   # a feature counts as "used by the model" above this
MIN_DISCRETE = 20       # features with at most this many distinct values are treated as categories


def _psi(expected, actual, floor=1e-4):
    expected, actual = np.maximum(expected, floor), np.maximum(actual, floor)
    return float(np.sum((actual - expected) * np.log(actual / expected)))


def psi(ref, cur, bins=10):
    """Population stability index of `cur` against `ref`: sum of (a - e) * ln(a / e) over bins."""
    if len(np.unique(ref)) <= MIN_DISCRETE:
        labels = np.unique(np.concatenate([ref, cur]))
        e = np.array([(ref == v).mean() for v in labels])
        a = np.array([(cur == v).mean() for v in labels])
    else:
        edges = np.quantile(ref, np.linspace(0, 1, bins + 1))
        edges[0], edges[-1] = -np.inf, np.inf
        e = np.histogram(ref, edges)[0] / len(ref)
        a = np.histogram(cur, edges)[0] / len(cur)
    return _psi(e, a)


def summarise(model, ref_cols, ref_score, reliance, cols, late, with_labels):
    score = model.predict_proba(design(cols))[:, 1]
    psis = {f: psi(ref_cols[f], cols[f]) for f in FEATURES}
    psis["score"] = psi(ref_score, score)
    used = {f: reliance[f] > RELIANCE_FLOOR for f in FEATURES}
    used["score"] = True
    expected = float(score.mean())
    window = {"rows": len(score), "psi": psis, "used": used, "expected": expected,
              "observed": None, "z": None, "gap": None}
    if with_labels:
        observed = float(late.mean())
        se = np.sqrt(expected * (1 - expected) / len(score))
        window.update(observed=observed, gap=observed - expected, z=(observed - expected) / se)
    return window


SHORT = {"distance_km": "dist", "order_value": "value", "carrier": "carr"}


def show(windows):
    columns = FEATURES + ["score"]
    print(f"{'window':<7}{'rows':>5} |" + " ".join(f"{SHORT.get(c, c):>6}" for c in columns)
          + f" |{'exp':>6} {'obs':>6} {'z':>5} | action")
    for name, w in windows.items():
        action, reasons = decide(w)
        observed = "--" if w["observed"] is None else f"{w['observed']:.3f}"
        z = "--" if w["z"] is None else f"{w['z']:+.1f}"
        print(f"{name:<7}{w['rows']:>5} |" + " ".join(f"{w['psi'][c]:>6.3f}" for c in columns)
              + f" |{w['expected']:>6.3f} {observed:>6} {z:>5} | {action}")
        for reason in reasons:
            print(f"          - {reason}")
    print("PSI columns per input and for the model score; exp = mean predicted late rate, obs = observed late rate, z = obs vs exp in standard errors")


def noise(model, ref_cols, ref_score, reliance):
    print("1. PSI between two samples of the same process (distance_km, 30 draws per size)")
    print(f"   {'rows':>6} {'median':>8} {'largest':>8}")
    for n in (100, 500, 2000, 8000):
        values = [psi(ref_cols["distance_km"], make_window(n, seed=1000 + i)[0]["distance_km"]) for i in range(30)]
        print(f"   {n:>6} {np.median(values):>8.3f} {max(values):>8.3f}")

    naive = tests = 0
    for week in range(52):
        cols, late = make_window(2000, seed=2000 + week)
        w = summarise(model, ref_cols, ref_score, reliance, cols, late, with_labels=False)
        naive += any(v > 0.10 for v in w["psi"].values())
        score = model.predict_proba(design(cols))[:, 1]
        pvalues = [ks_2samp(ref_cols[f], cols[f]).pvalue for f in ("distance_km", "order_value")]
        pvalues.append(ks_2samp(ref_score, score).pvalue)
        tests += any(p < 0.05 for p in pvalues)
    print("\n2. 52 weeks in which nothing changed (2000 rows each)")
    print(f"   {'alert rule':<46} {'weeks alerted':>13}")
    print(f"   {'any PSI above 0.10':<46} {naive:>13}")
    print(f"   {'any KS test p < 0.05 (distance, value, score)':<46} {tests:>13}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--labels", action="store_true")
    parser.add_argument("--noise", action="store_true")
    args = parser.parse_args()

    model, ref_cols, ref_late, reliance = fit_reference()
    ref_score = model.predict_proba(design(ref_cols))[:, 1]
    if args.noise:
        return noise(model, ref_cols, ref_score, reliance)
    print(f"training window: {len(ref_late)} rows, late rate {ref_late.mean():.3f}, mean score {ref_score.mean():.3f}")
    windows = {name: summarise(model, ref_cols, ref_score, reliance, cols, late, args.labels)
               for name, (cols, late) in later_windows().items()}
    show(windows)


if __name__ == "__main__":
    main()
