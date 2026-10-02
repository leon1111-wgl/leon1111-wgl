# Guoliang | Original learning example
# Count alerts and misses
# Python 3.12+ | Run: python evaluation-shift-evaluate-alerts.py
true_positive, false_positive, false_negative = 15, 10, 5
precision = true_positive / (true_positive + false_positive)
recall = true_positive / (true_positive + false_negative)
f1 = 2 * true_positive / (2 * true_positive + false_positive + false_negative)
print(f"precision={precision:.2f}; recall={recall:.2f}; F1={f1:.4f}")
sessions = {"train": {"morning-A", "evening-A"}, "test": {"morning-B"}}
print("shared sessions:", len(sessions["train"] & sessions["test"]))
