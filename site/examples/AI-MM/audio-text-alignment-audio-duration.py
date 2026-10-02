# Guoliang | Original learning example
# Check the time before matching
# Python 3.12+ | Run: python audio-text-alignment-audio-duration.py
duration = 4
original_rate = 48000
new_rate = 16000
original_count = duration * original_rate
new_count = duration * new_rate
print("counts:", original_count, new_count)
print("wrong relabelled duration:", original_count / new_rate)
audio = [0.8, 0.6]
text = [0.6, 0.8]
print(f"similarity={sum(a * b for a, b in zip(audio, text)):.2f}")
