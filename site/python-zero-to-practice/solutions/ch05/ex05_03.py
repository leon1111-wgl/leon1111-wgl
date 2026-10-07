# 第 05_03 题 学习打卡统计
# 学习分钟数 [0, 30, 45, 0, 60]，分别输出学习过的天数 3 和总分钟 135。
# 预期程序输出：
# 3
# 135

days = 0
total = 0
for minutes in [0, 30, 45, 0, 60]:
    if minutes > 0:
        days += 1
    total += minutes
print(days)
print(total)
