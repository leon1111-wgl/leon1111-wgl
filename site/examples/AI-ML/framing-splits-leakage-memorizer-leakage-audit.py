# Leon | Original learning example
# Expose leakage with a deliberately simple memorizer
# Python 3.12+ | Run: python framing-splits-leakage-memorizer-leakage-audit.py
rows = [(device, label) for device, label in
        [("A", 0), ("B", 1), ("C", 0), ("D", 1)] for _ in range(2)]

def evaluate(train, test):
    memory = {device: label for device, label in train}
    fallback = int(sum(label for _, label in train) > len(train) / 2)
    predictions = [memory.get(device, fallback) for device, _ in test]
    accuracy = sum(p == label for p, (_, label) in zip(predictions, test)) / len(test)
    overlap = {d for d, _ in train} & {d for d, _ in test}
    return accuracy, sorted(overlap)

row_train, row_test = rows[::2], rows[1::2]
group_train = [row for row in rows if row[0] in {"A", "B"}]
group_test = [row for row in rows if row[0] in {"C", "D"}]
row_score, overlap = evaluate(row_train, row_test)
group_score, clean_overlap = evaluate(group_train, group_test)
assert row_score == 1.0 and group_score == 0.5 and not clean_overlap
print(f"row split: accuracy={row_score:.2f}; shared devices={overlap}")
print(f"group split: accuracy={group_score:.2f}; shared devices={clean_overlap}")
