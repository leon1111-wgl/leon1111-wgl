# Guoliang | Original learning example
# Sample a video and compare intervals
# Python 3.12+ | Run: python video-temporal-grounding-temporal-overlap.py
timestamps = list(range(0, 12, 2))
short_event = (5.2, 5.7)
seen = any(short_event[0] <= t <= short_event[1] for t in timestamps)
predicted = (5, 9)
reference = (4, 8)
intersection = max(0, min(predicted[1], reference[1]) - max(predicted[0], reference[0]))
union = (predicted[1] - predicted[0]) + (reference[1] - reference[0]) - intersection
print("sample times:", timestamps)
print("short event sampled:", seen)
print(f"temporal IoU={intersection / union:.2f}")
