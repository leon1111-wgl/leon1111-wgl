# Leon | Original learning example
# An iterator for a circular queue
# Python 3.12+ | Run: python stack-queue-applications-ring-queue-iterator.py
class RingQueue:
    def __init__(self, capacity):
        self.slots = [None] * capacity
        self.front = 0
        self.size = 0
        self.version = 0                  # changes on every enqueue or dequeue

    def enqueue(self, item):
        if self.size == len(self.slots):
            raise OverflowError("queue is full")
        self.slots[(self.front + self.size) % len(self.slots)] = item
        self.size += 1
        self.version += 1

    def dequeue(self):
        item = self.slots[self.front]
        self.slots[self.front] = None
        self.front = (self.front + 1) % len(self.slots)
        self.size -= 1
        self.version += 1
        return item

    def __iter__(self):
        return RingIterator(self)

class RingIterator:
    def __init__(self, queue):
        self.queue = queue
        self.seen = 0                     # how many items were already returned
        self.expected = queue.version

    def __iter__(self):
        return self

    def __next__(self):
        if self.queue.version != self.expected:
            raise RuntimeError("queue changed during iteration")
        if self.seen == self.queue.size:
            raise StopIteration
        slot = (self.queue.front + self.seen) % len(self.queue.slots)
        self.seen += 1
        return self.queue.slots[slot]

q = RingQueue(4)
for name in ["Leon", "Mia", "Emma", "Jack"]:
    q.enqueue(name)
q.dequeue()
q.enqueue("Noah")                         # wraps to slot 0
print("slots:", q.slots, " front:", q.front)
print("in order:", [name for name in q], " size:", q.size)

first, second = iter(q), iter(q)
print(next(first), next(first), next(second))

try:
    for name in q:
        print("visiting", name)
        q.dequeue()
except RuntimeError as error:
    print("error:", error)
