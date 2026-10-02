# Guoliang | Original learning example
# Follow a bounded cuckoo insertion
# Python 3.12+ | Run: python cuckoo-maps-sets-cuckoo-two-home-demo.py
first = [None] * 3
second = [None] * 3
def insert(key):
    board = 0
    for _ in range(8):
        table = first if board == 0 else second
        index = key % 3 if board == 0 else (key // 3) % 3
        table[index], key = key, table[index]
        if key is None:
            return
        board = 1 - board
    raise RuntimeError("Rebuild required; an evicted key remains")
for key in [0, 3, 6]:
    insert(key)
print("first:", first)
print("second:", second)
print("3 found:", first[3 % 3] == 3 or second[(3 // 3) % 3] == 3)
