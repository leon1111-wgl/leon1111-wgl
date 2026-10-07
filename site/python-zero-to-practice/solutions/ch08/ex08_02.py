# 第 08_02 题 字母次数
# 统计 banana 每个字母出现次数，输出字典 {"b":1,"a":3,"n":2} 对应的 Python 表示。
# 预期程序输出：
# {'b': 1, 'a': 3, 'n': 2}

counts = {}
for char in "banana":
    counts[char] = counts.get(char, 0) + 1
print(counts)
