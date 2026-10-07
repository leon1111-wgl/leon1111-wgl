# 最小计数器
class Counter:
    def __init__(self, start=0):
        self.value = start

    def add(self, amount=1):
        self.value += amount

counter = Counter(3)
counter.add()
counter.add(2)
print(counter.value)
