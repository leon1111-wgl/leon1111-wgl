# Guoliang | Original learning example
# Build the tree and read its codewords
# Python 3.12+ | Run: python huffman-coding-huffman-tree-codebook.py
import heapq
from itertools import count
frequencies = {"A": 12, "B": 7, "C": 4, "D": 2}
serial = count()
heap = [(freq, next(serial), (symbol, None, None))
        for symbol, freq in frequencies.items()]
heapq.heapify(heap)
merges = []
while len(heap) > 1:
    a, _, left = heapq.heappop(heap)
    b, _, right = heapq.heappop(heap)
    merges.append(a + b)
    heapq.heappush(heap, (a + b, next(serial), (None, left, right)))
codes = {}
def walk(node, prefix):
    symbol, left, right = node
    if symbol is not None:
        codes[symbol] = prefix
        return
    walk(left, prefix + "0")
    walk(right, prefix + "1")
walk(heap[0][2], "")
for symbol in sorted(codes):
    print(symbol, codes[symbol])
print("merges:", merges)
print("bits:", sum(frequencies[s] * len(codes[s]) for s in codes))
