# 第 07_04 题 移动末尾任务
# tasks = ["A", "B", "C"]，把最后一个移动到最前，输出 ["C", "A", "B"] 对应的 Python 列表表示。
# 预期程序输出：
# ['C', 'A', 'B']

tasks = ["A", "B", "C"]
last = tasks.pop()
tasks.insert(0, last)
print(tasks)
