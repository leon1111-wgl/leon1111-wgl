# 第 14_02 题 学习记录平均值
# 实现 StudyLog 类，实例 minutes 为空列表，add(value) 追加，mean() 空时 None，否则平均值。添加 30、60 后打印 mean()。
# 预期程序输出：
# 45.0

class StudyLog:
    def __init__(self):
        self.minutes = []

    def add(self, value):
        self.minutes.append(value)

    def mean(self):
        if not self.minutes:
            return None
        return sum(self.minutes) / len(self.minutes)

log = StudyLog()
log.add(30)
log.add(60)
print(log.mean())
