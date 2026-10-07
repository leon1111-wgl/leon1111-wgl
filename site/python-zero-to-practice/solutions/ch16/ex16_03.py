# 第 16_03 题 未知词编码
# 实现 encode(text,vocab)，按空白拆词，用 vocab["<UNK>"] 处理未知词。打印 "a x" 在 {"<UNK>":1,"a":2} 下的结果。
# 预期程序输出：
# [2, 1]

def encode(text, vocab):
    return [vocab.get(word, vocab["<UNK>"]) for word in text.split()]

print(encode("a x", {"<UNK>": 1, "a": 2}))
