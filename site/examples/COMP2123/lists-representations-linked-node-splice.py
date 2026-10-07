# Leon | Original learning example
# Insert a real node into a linked chain
# Python 3.12+ | Run: python lists-representations-linked-node-splice.py
class Node:
    def __init__(self, value, next_node=None):
        self.value = value
        self.next = next_node

n = Node("N")
m = Node("M", n)
head = Node("L", m)
old_next = m.next
m.next = Node("X", old_next)
values = []
current = head
while current is not None:
    values.append(current.value)
    current = current.next
print(values)
print("X still links to N:", m.next.next is n)
