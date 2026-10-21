# 第 06_08 题 AI / Agent：完成前先扣减工作量
# 给定 remaining = 5、steps = 0。每轮处理一项，remaining 减 1，steps 加 1；只要有剩余且 steps 小于 3 就继续。最后分别输出 steps、remaining。不要写无限循环。
# 预期程序输出：
# 3
# 2

remaining = 5
steps = 0
while remaining > 0 and steps < 3:
    remaining -= 1
    steps += 1
print(steps)
print(remaining)
