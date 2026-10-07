# 第 05_04 题 单词长度报告
# 对 ["cat", "python", "AI"] 输出 cat:3、python:6、AI:2，各占一行。
# 预期程序输出：
# cat:3
# python:6
# AI:2

for word in ["cat", "python", "AI"]:
    print(f"{word}:{len(word)}")
