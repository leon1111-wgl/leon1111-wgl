# Leon | Original learning example
# Watch the call stack grow and overflow
# Python 3.12+ | Run: python stack-queue-applications-call-stack-frames.py
class CallStack:
    """A tiny model of the memory that holds one frame per active call."""
    def __init__(self, capacity):
        self.frames = []
        self.capacity = capacity

    def push(self, name):
        if len(self.frames) == self.capacity:
            raise OverflowError("stack overflow while calling " + name)
        self.frames.append(name)

    def pop(self):
        self.frames.pop()

def recursive_sum(n, stack, log):
    stack.push("sum(" + str(n) + ")")
    if log:
        print("enter:", " > ".join(stack.frames))
    result = 0 if n == 0 else n + recursive_sum(n - 1, stack, log)
    if log:
        print("leave:", " > ".join(stack.frames), "returns", result)
    stack.pop()
    return result

def loop_sum(n):
    total = 0                    # one frame only: the answer lives in a variable
    for i in range(1, n + 1):
        total += i
    return total

print("answer:", recursive_sum(3, CallStack(10), True))
for n in [2, 3, 6]:
    try:
        print("capacity 4, n =", n, "->", recursive_sum(n, CallStack(4), False))
    except OverflowError as error:
        print("capacity 4, n =", n, "->", error)
print("loop version, n = 6 ->", loop_sum(6))
