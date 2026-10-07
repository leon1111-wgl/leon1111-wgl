# 第 16_02 题 训练词表
# 实现 build_vocab(texts)，初始 {"<PAD>":0,"<UNK>":1}，按首次出现为按空白分出的词分配 ID；文本已预处理。打印 ["a b","a c"] 的结果。
# 预期程序输出：
# {'<PAD>': 0, '<UNK>': 1, 'a': 2, 'b': 3, 'c': 4}

def build_vocab(texts):
    vocab = {"<PAD>": 0, "<UNK>": 1}
    for text in texts:
        for word in text.split():
            if word not in vocab:
                vocab[word] = len(vocab)
    return vocab

print(build_vocab(["a b", "a c"]))
