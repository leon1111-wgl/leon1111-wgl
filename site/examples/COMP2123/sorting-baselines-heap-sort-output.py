# Leon | Original learning example
# Sort by repeatedly removing a heap minimum
# Python 3.12+ | Run: python sorting-baselines-heap-sort-output.py
import heapq
values = [5, 2, 4, 1]
heap = values.copy()
heapq.heapify(heap)
result = []
while heap:
    result.append(heapq.heappop(heap))
print("input:", values)
print("sorted:", result)
