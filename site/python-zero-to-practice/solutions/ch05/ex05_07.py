# 第 05_07 题 最长单词
# 在 ["I","study","python","daily"] 中找第一个最长词，输出 python；不用 max。
# 预期程序输出：
# python

words = ["I", "study", "python", "daily"]
longest = ""
for word in words:
    if len(word) > len(longest):
        longest = word
print(longest)
