# 第 07_06 题 按顺序去重
# 对 ["a","b","a","c","b"] 去重并保留首次出现顺序，输出 ["a","b","c"] 的列表表示。
# 预期程序输出：
# ['a', 'b', 'c']

unique = []
for item in ["a", "b", "a", "c", "b"]:
    if item not in unique:
        unique.append(item)
print(unique)
