# Leon | Original learning example
# Lists, positions and repeated steps
# Python 3.12+ | Run: python lists-loops-first-steps.py
values = [18, 21, 24]
total = 0
for value in values:
    total = total + value
    print("running total:", total)
print("first:", values[0])
print("mean:", total / len(values))
