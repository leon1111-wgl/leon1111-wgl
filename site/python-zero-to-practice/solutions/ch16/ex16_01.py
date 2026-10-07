# 第 16_01 题 文本清洗函数
# 实现 normalize(text)，转小写并将连续空白变成单空格，去两端空白。打印对 "  Hello   AI  " 的结果。
# 预期程序输出：
# hello ai

def normalize(text):
    return " ".join(text.lower().split())

print(normalize("  Hello   AI  "))
