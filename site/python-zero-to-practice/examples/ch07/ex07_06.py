# 二维列表共享陷阱
bad = [[0] * 2] * 2
bad[0][0] = 9
print(bad)
good = []
for _ in range(2):
    good.append([0] * 2)
good[0][0] = 9
print(good)
