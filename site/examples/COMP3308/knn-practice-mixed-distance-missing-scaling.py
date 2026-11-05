# Leon | Original learning example
# Mixed distance, missing values and scaling
# Python 3.12+ | Run: python knn-practice-mixed-distance-missing-scaling.py
from math import ceil, log2, sqrt

# Clinic records: (age, distance in km, reminder, outcome). None marks a missing value.
train = [(25, 2, "sms", "came"), (65, 12, "none", "missed"), (45, None, "sms", "missed"),
         (35, 10, "none", "missed"), (55, 4, "email", "came")]
query = (45, 8, "sms")
NUMBER_COLUMNS = (0, 1)           # column 2 is a category


def fit_ranges(rows):
    """Smallest and largest known value of each number column, from training rows only."""
    ranges = {}
    for col in NUMBER_COLUMNS:
        known = [row[col] for row in rows if row[col] is not None]
        ranges[col] = (min(known), max(known))
    return ranges


def column_gaps(a, b, ranges):
    gaps = []
    for col in range(3):
        if a[col] is None or b[col] is None:
            gaps.append(None)                      # unknown
        elif col in NUMBER_COLUMNS:
            low, high = ranges[col]
            gaps.append(abs(a[col] - b[col]) / (high - low))
        else:
            gaps.append(0.0 if a[col] == b[col] else 1.0)
    return gaps


def distance(a, b, ranges, policy):
    gaps = column_gaps(a, b, ranges)
    known = [g for g in gaps if g is not None]
    if policy == "penalty":                        # an unknown column counts as the largest gap, 1
        return sqrt(sum(g * g for g in known) + (len(gaps) - len(known)))
    return sqrt(sum(g * g for g in known) * len(gaps) / len(known))   # skip it and rescale


ranges = fit_ranges(train)
print("ranges:", ranges)
for policy in ("penalty", "rescale"):
    ranked = sorted((distance(query, row, ranges, policy), i + 1, row[3]) for i, row in enumerate(train))
    print(policy, [f"r{i}={d:.3f}" for d, i, _ in ranked])
    for k in (1, 3):
        votes = [label for _, _, label in ranked[:k]]
        print(f"  k={k}: {max(set(votes), key=votes.count)}")

# Scaling: age in years next to distance in metres.
rows = [(25, 500), (65, 12000), (25, 7900), (46, 6000)]
spans = [(min(c), max(c)) for c in zip(*rows)]
q, a, b = (45, 8000), rows[2], rows[3]
raw = [sqrt(sum((x - y) ** 2 for x, y in zip(q, r))) for r in (a, b)]
scaled = [sqrt(sum(((x - y) / (hi - lo)) ** 2 for x, y, (lo, hi) in zip(q, r, spans))) for r in (a, b)]
print(f"unscaled: A={raw[0]:.2f} B={raw[1]:.2f} -> nearest is {'A' if raw[0] < raw[1] else 'B'}")
print(f"scaled:   A={scaled[0]:.3f} B={scaled[1]:.3f} -> nearest is {'A' if scaled[0] < scaled[1] else 'B'}")
print("a new person aged 80 scales to", (80 - spans[0][0]) / (spans[0][1] - spans[0][0]))

# Lazy learning: all the work is paid at query time.
stored, features, queries = 100_000, 50, 1_000
print(f"one query reads {stored * features:,} numbers; {queries:,} queries read {stored * features * queries:,}")
print("a balanced tree over the same examples is", ceil(log2(stored)), "questions deep")
