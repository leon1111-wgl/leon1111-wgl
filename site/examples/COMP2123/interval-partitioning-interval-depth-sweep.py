# Leon | Original learning example
# Independently certify the room lower bound
# Python 3.12+ | Run: python interval-partitioning-interval-depth-sweep.py
sessions = [(1, 4), (2, 5), (4, 6), (5, 7)]
events = []
for start, finish in sessions:
    events.append((start, 1))
    events.append((finish, -1))
active = depth = 0
for time, change in sorted(events):
    active += change
    depth = max(depth, active)
    print(time, change, active)
print("minimum rooms:", depth)
