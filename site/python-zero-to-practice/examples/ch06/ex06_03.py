# 跳过无效项
total = 0
for value in [10, -1, 20, -5, 30]:
    if value < 0:
        continue
    total += value
print(total)
