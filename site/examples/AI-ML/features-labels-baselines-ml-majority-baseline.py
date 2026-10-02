# Guoliang | Original learning example
# Build a majority-label baseline
# Python 3.12+ | Run: python features-labels-baselines-ml-majority-baseline.py
from collections import Counter
train_y = [0, 0, 0, 1]
test_y = [0, 1, 1, 0]
counts = Counter(train_y)
baseline = min(counts, key=lambda label: (-counts[label], label))
predictions = [baseline] * len(test_y)
correct = sum(pred == true for pred, true in zip(predictions, test_y))
print('baseline class:', baseline)
print('predictions:', predictions)
print(f'test accuracy: {correct / len(test_y):.2f}')
