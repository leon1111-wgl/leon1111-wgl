# Leon | Original learning example
# Count a changed word
# Python 3.12+ | Run: python speech-tasks-word-error-rate.py
reference = "bring the new box".split()
substitutions, deletions, insertions = 1, 0, 0
wer = (substitutions + deletions + insertions) / len(reference)
print("reference words:", len(reference))
print(f"WER={wer:.2f}")
short_reference_count = 2
print(f"three insertions WER={3 / short_reference_count:.2f}")
