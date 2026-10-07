# 第 07_01 题 保留合格成绩
# 从 [30, 60, 85, 59] 中生成新列表 [60, 85]，并输出。不要修改遍历中的原列表。
# 预期程序输出：
# [60, 85]

passed = []
for score in [30, 60, 85, 59]:
    if score >= 60:
        passed.append(score)
print(passed)
