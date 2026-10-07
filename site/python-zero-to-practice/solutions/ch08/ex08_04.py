# 第 08_04 题 检测重复 ID
# ids = ["s1","s2","s1","s3"]。若有重复输出 True，否则 False。
# 预期程序输出：
# True

ids = ["s1", "s2", "s1", "s3"]
print(len(ids) != len(set(ids)))
