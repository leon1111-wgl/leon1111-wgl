# Leon | Original learning example
# Write the heap insertion repair
# Python 3.12+ | Run: python priority-queues-heaps-heap-bubble-up.py
heap = [3, 8, 5, 12, 10]
heap.append(4)
i = len(heap) - 1
swaps = 0
while i > 0:
    parent = (i - 1) // 2
    if heap[parent] <= heap[i]:
        break
    heap[parent], heap[i] = heap[i], heap[parent]
    i = parent
    swaps += 1
print(heap)
print("swaps:", swaps)
print("valid:", all(heap[(j - 1) // 2] <= heap[j] for j in range(1, len(heap))))
