# Guoliang | Original learning example
# Functions, choices and small checks
# Python 3.12+ | Run: python functions-tests-first-steps.py
def label_temperature(value):
    if value >= 25:
        return "warm"
    return "cool"

assert label_temperature(24) == "cool"
assert label_temperature(25) == "warm"
for reading in [24, 25, 29]:
    print(reading, label_temperature(reading))
