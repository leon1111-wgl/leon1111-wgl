# 第 03_03 题 提取文件扩展名
# 给定 filename = "report.final.csv"，按点拆分，输出最后一部分 csv。
# 预期程序输出：
# csv

filename = "report.final.csv"
print(filename.split(".")[-1])
