# Guoliang | Original learning example
# Read three ranked detections
# Python 3.12+ | Run: python detection-average-precision-ranked-ap.py
matches = [True, False, True]
reference_count = 2
found = 0
ap = 0.0
for rank, correct in enumerate(matches, start=1):
    found += int(correct)
    precision = found / rank
    recall = found / reference_count
    if correct:
        ap += precision / reference_count
    print(f"rank={rank}: precision={precision:.4f}, recall={recall:.4f}")
print(f"toy AP={ap:.4f}")
