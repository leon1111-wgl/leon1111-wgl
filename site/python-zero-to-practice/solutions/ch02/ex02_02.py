# 第 02_02 题 时间拆分
# 把 3671 秒拆成小时、分钟、秒，并用空格分隔输出 1 1 11。
# 预期程序输出：
# 1 1 11

seconds = 3671
hours = seconds // 3600
minutes = (seconds % 3600) // 60
remaining = seconds % 60
print(hours, minutes, remaining)
