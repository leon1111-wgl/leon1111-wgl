# 第 04_06 题 区分未填和零
# value = 0，None 表示未填，其他数值包括 0 都算已填。输出 已填。
# 预期程序输出：
# 已填

value = 0
if value is None:
    print("未填")
else:
    print("已填")
