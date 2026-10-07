# 第 11_01 题 均值与中位数
# 用 statistics 模块计算 [1,2,100] 的 mean 和 median，分别输出并把均值格式化为两位小数。
# 预期程序输出：
# 34.33
# 2

import statistics
values = [1, 2, 100]
print(f"{statistics.mean(values):.2f}")
print(statistics.median(values))
