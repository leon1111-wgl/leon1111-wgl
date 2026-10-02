# Guoliang | Original learning example
# Count unsupported mentions and coverage
# Python 3.12+ | Run: python evaluation-hallucination-claim-audit.py
mentions, unsupported = 40, 6
captions, captions_with_error = 10, 4
correct_distinct, target_objects = 34, 50
print(f"unsupported mention rate={unsupported / mentions:.2f}")
print(f"captions with errors={captions_with_error / captions:.2f}")
print(f"target coverage={correct_distinct / target_objects:.2f}")
print(f"short revision coverage={19 / target_objects:.2f}")
