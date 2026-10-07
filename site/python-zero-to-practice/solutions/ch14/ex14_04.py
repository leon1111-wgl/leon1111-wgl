# 第 14_04 题 只接受有效分数
# 实现 GradeBook，实例 scores=[]，add(score) 接受 0—100 的整数，越界抛 ValueError 且不修改状态。这里只要求范围验证。添加 80 后打印 scores。
# 预期程序输出：
# [80]

class GradeBook:
    def __init__(self):
        self.scores = []

    def add(self, score):
        if not 0 <= score <= 100:
            raise ValueError("分数超出范围")
        self.scores.append(score)

book = GradeBook()
book.add(80)
print(book.scores)
