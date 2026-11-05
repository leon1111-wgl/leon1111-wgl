"""Confusion matrix on the validation set at one threshold.  Usage: python3 confusion.py [THRESHOLD]"""
import sys

from sklearn.metrics import confusion_matrix, roc_auc_score

from fraud import MISSED_COST, REVIEW_COST, cost, fit, scores, splits

threshold = float(sys.argv[1]) if len(sys.argv) > 1 else 0.5
(X_train, y_train), (X_val, y_val), _test_stays_closed = splits()
score = scores(fit(X_train, y_train), X_val)
flagged = score >= threshold

tn, fp, fn, tp = confusion_matrix(y_val, flagged).ravel()
print(f"validation: {len(y_val)} payments, {y_val.sum()} fraud, ROC AUC {roc_auc_score(y_val, score):.3f}")
print(f"threshold {threshold}: flag a payment when its score is at least this")
print("                 predicted ok   predicted fraud")
print(f"actual ok        {tn:>12}   {fp:>15}")
print(f"actual fraud     {fn:>12}   {tp:>15}")
print(f"accuracy {(tn + tp) / len(y_val):.3f}   precision {tp / max(tp + fp, 1):.3f}   recall {tp / (tp + fn):.3f}")
print(f"cost {cost(y_val, flagged):,.0f}   "
      f"(flag nothing {MISSED_COST * y_val.sum():,.0f}, flag everything {REVIEW_COST * len(y_val):,.0f})")
