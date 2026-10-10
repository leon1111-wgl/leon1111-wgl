# Leon | Original learning example
# Choose a decision threshold with an explicit error cost
# Python 3.12+ | Run: python logistic-thresholds-validation-cost-threshold.py
scores = [0.10, 0.35, 0.45, 0.60, 0.80]
truth = [0, 1, 0, 1, 1]

def cost_at(threshold):
    predicted = [int(score >= threshold) for score in scores]
    fp = sum(p == 1 and y == 0 for p, y in zip(predicted, truth))
    fn = sum(p == 0 and y == 1 for p, y in zip(predicted, truth))
    return fp + 4 * fn, fp, fn

candidates = [0.30, 0.50, 0.70, 1.10]
for threshold in candidates:
    cost, fp, fn = cost_at(threshold)
    print(f"threshold={threshold:.2f} FP={fp} FN={fn} cost={cost}")
best = min(candidates, key=lambda t: (cost_at(t)[0], t))
assert best == 0.30 and cost_at(best) == (1, 1, 0)
print(f"selected on validation: {best:.2f}")
