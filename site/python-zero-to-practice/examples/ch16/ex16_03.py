# 训练词表与未知词
train_texts = ["hello python", "hello world"]
vocab = {"<PAD>": 0, "<UNK>": 1}
for text in train_texts:
    for word in text.split():
        if word not in vocab:
            vocab[word] = len(vocab)
encoded = [vocab.get(word, vocab["<UNK>"]) for word in "hello ai".split()]
print(vocab)
print(encoded)
