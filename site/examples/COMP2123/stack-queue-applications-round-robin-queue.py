# Leon | Original learning example
# Share a processor fairly with a queue
# Python 3.12+ | Run: python stack-queue-applications-round-robin-queue.py
from collections import deque

def round_robin(jobs, quantum, show):
    queue = deque(jobs)                  # (name, time still needed)
    clock = 0
    first_turn, finish = {}, {}
    while queue:
        name, left = queue.popleft()
        run = min(quantum, left)
        first_turn.setdefault(name, clock)
        if show:
            print("t =", clock, name, "runs", run)
        clock += run
        if left > run:
            queue.append((name, left - run))     # back of the line
        else:
            finish[name] = clock
    return first_turn, finish

jobs = [("Leon", 5), ("Mia", 3), ("Emma", 1)]
first_turn, finish = round_robin(jobs, 2, True)
print("quantum 2  first turns:", first_turn, " finish:", finish)
first_turn, finish = round_robin(jobs, 100, False)
print("quantum 100 first turns:", first_turn, " finish:", finish)
