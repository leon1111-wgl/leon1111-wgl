# Leon | Original learning example
# Locate the largest change
# Python 3.12+ | Run: python defect-inspection-difference-inspection.py
reference = [10, 10, 10, 10]
observed = [11, 9, 25, 10]
differences = [abs(x - r) for x, r in zip(observed, reference)]
flagged = [i for i, value in enumerate(differences) if value > 5]
print("differences:", differences)
print("flagged positions:", flagged)
print("image score:", max(differences))
