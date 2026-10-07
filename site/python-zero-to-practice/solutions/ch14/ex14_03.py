# 第 14_03 题 可索引的记录集
# 实现 NumberDataset 类，构造时复制 values 到实例，支持 len 和 [index]。用 [10,20] 创建后依次打印长度与索引 0 的值。
# 预期程序输出：
# 2
# 10

class NumberDataset:
    def __init__(self, values):
        self.values = list(values)

    def __len__(self):
        return len(self.values)

    def __getitem__(self, index):
        return self.values[index]

data = NumberDataset([10, 20])
print(len(data))
print(data[0])
