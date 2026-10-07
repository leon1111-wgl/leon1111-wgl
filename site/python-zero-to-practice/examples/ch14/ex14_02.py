# 实例各自保存记录
class StudyLog:
    def __init__(self):
        self.minutes = []

    def add(self, value):
        self.minutes.append(value)

    def total(self):
        return sum(self.minutes)

a = StudyLog()
b = StudyLog()
a.add(30)
print(a.total(), b.total())
