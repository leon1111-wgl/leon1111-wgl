# 简单继承
class Reporter:
    def describe(self):
        return "普通报告"

class StudyReporter(Reporter):
    def describe(self):
        return "学习报告"

print(Reporter().describe())
print(StudyReporter().describe())
