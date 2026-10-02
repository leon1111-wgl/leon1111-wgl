# Guoliang | Original learning example
# Serve waiting jobs with deque
# Python 3.12+ | Run: python stacks-queues-deque-fifo-service.py
from collections import deque
queue = deque(["Ada", "Bo"])
queue.append("Cy")
print("served:", queue.popleft())
print("waiting:", list(queue))
queue.appendleft("urgent")
print("left end:", queue.popleft())
print("waiting:", list(queue))
