# Leon | Original learning example
# Find a delayed clap
# Python 3.12+ | Run: python audio-video-sync-sync-offset.py
visual = [0, 1, 0, 0, 0]
audio = [0, 0, 1, 0, 0]
scores = {}
for shift in [-1, 0, 1]:
    total = 0
    for t in range(len(visual)):
        j = t + shift
        if 0 <= j < len(audio):
            total += visual[t] * audio[j]
    scores[shift] = total
best_shift = max(scores, key=scores.get)
print("shift scores:", scores)
print(f"audio delay seconds={best_shift * 0.1:.1f}")
