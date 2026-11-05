# Leon | Original learning example
# Add a minimum() operation to a stack
# Python 3.12+ | Run: python augmenting-structures-min-stack-adt.py
class WrongMinStack:
    """Remembers one smallest value for the whole stack."""
    def __init__(self):
        self.items = []
        self.smallest = None

    def push(self, value):
        self.items.append(value)
        if self.smallest is None or value < self.smallest:
            self.smallest = value

    def pop(self):
        return self.items.pop()               # smallest is never repaired

class MinStack:
    """Each item also stores the smallest value at or below it."""
    def __init__(self):
        self.items = []                       # pairs (value, smallest so far)

    def push(self, value):
        smallest = value if not self.items else min(value, self.items[-1][1])
        self.items.append((value, smallest))

    def pop(self):
        return self.items.pop()[0]

    def minimum(self):
        return self.items[-1][1]

wrong, good = WrongMinStack(), MinStack()
for value in [5, 3, 7, 3, 8]:
    wrong.push(value)
    good.push(value)
    print("push", value, " minimum:", good.minimum())

for _ in range(4):
    popped = good.pop()
    wrong.pop()
    print("pop", popped, " minimum:", good.minimum(), " one-variable version says:", wrong.smallest)
