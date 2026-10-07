# Leon | Original learning example
# Use heapq to serve priorities
# Python 3.12+ | Run: python priority-queues-heaps-heapq-priority-service.py
import heapq
jobs = [8, 3, 5, 12, 10]
heapq.heapify(jobs)
print("minimum:", jobs[0])
heapq.heappush(jobs, 4)
served = []
while jobs:
    served.append(heapq.heappop(jobs))
print("served:", served)
