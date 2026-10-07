# 第 14_01 题 步数计数器
# 实现 StepCounter 类，初始 steps=0，add(count) 累加步数；本题 count 约定非负整数。创建对象加 100 再加 50，打印 steps。
# 预期程序输出：
# 150

class StepCounter:
    def __init__(self):
        self.steps = 0

    def add(self, count):
        self.steps += count

counter = StepCounter()
counter.add(100)
counter.add(50)
print(counter.steps)
