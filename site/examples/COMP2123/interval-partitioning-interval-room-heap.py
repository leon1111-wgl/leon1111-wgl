# Leon | Original learning example
# Assign every session to a room
# Python 3.12+ | Run: python interval-partitioning-interval-room-heap.py
import heapq
sessions = [(1, 4, "A"), (2, 5, "B"), (4, 6, "C"), (5, 7, "D")]
heap = []
rooms = 0
for start, finish, name in sorted(sessions):
    if heap and heap[0][0] <= start:
        _, room = heapq.heappop(heap)
    else:
        rooms += 1
        room = rooms
    heapq.heappush(heap, (finish, room))
    print(name, "room", room)
print("rooms:", rooms)
