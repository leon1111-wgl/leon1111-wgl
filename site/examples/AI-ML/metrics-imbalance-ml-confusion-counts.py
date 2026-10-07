# Leon | Original learning example
# Compute four metrics from counts
# Python 3.12+ | Run: python metrics-imbalance-ml-confusion-counts.py
tp, tn, fp, fn = 8, 78, 12, 2
total = tp + tn + fp + fn
accuracy = (tp + tn) / total
precision = tp / (tp + fp)
recall = tp / (tp + fn)
f1 = 2 * tp / (2 * tp + fp + fn)
for name, value in [('accuracy', accuracy), ('precision', precision),
                    ('recall', recall), ('F1', f1)]:
    print(f'{name}: {value:.3f}')
print('clips to review:', tp + fp)
