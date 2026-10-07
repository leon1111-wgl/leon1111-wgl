# 数据集接口预习
class TextDataset:
    def __init__(self, texts):
        self.texts = list(texts)

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, index):
        return self.texts[index]

dataset = TextDataset(["hello", "python"])
print(len(dataset))
print(dataset[1])
