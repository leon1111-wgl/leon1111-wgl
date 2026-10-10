# Leon | Original learning example
# Align events with timestamps, offsets and a tolerance
# Python 3.12+ | Run: python audio-video-sync-timestamp-nearest-alignment.py
from bisect import bisect_left
from math import isclose

def nearest_frame(timestamps, event_time, offset, tolerance):
    if tolerance < 0 or not timestamps:
        raise ValueError("nonempty timestamps and nonnegative tolerance required")
    if any(a >= b for a, b in zip(timestamps, timestamps[1:])):
        raise ValueError("frame timestamps must be strictly increasing")
    target = event_time - offset  # audio_time = video_time + offset
    insertion = bisect_left(timestamps, target)
    candidates = [i for i in (insertion - 1, insertion) if 0 <= i < len(timestamps)]
    best = min(candidates, key=lambda i: (abs(timestamps[i] - target), i))
    error = abs(timestamps[best] - target)
    return (best, error) if error <= tolerance else None

video = [0.0, 0.041, 0.083, 0.126, 0.168]
events = [0.061, 0.104, 0.300]
matches = [nearest_frame(video, event, 0.020, 0.010) for event in events]
assert matches[0][0] == 1 and isclose(matches[0][1], 0.0, abs_tol=1e-12)
assert matches[1][0] == 2 and isclose(matches[1][1], 0.001)
assert matches[2] is None
assert nearest_frame([0.0, 2.0], 1.0, 0.0, 1.0)[0] == 0
for event, match in zip(events, matches):
    if match is None:
        print(f"audio {event:.3f}: unmatched")
    else:
        index, error = match
        print(f"audio {event:.3f}: frame {index}, error {error:.3f} s")
