# 第 06_04 题 限次查找
# 给定 guesses = [2, 4, 7, 9]，目标是 7，输出第几次猜中：3。
# 预期程序输出：
# 3

for attempt, guess in enumerate([2, 4, 7, 9], start=1):
    if guess == 7:
        print(attempt)
        break
