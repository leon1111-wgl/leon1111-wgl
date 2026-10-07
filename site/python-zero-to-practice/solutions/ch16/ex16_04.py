# 第 16_04 题 准确率函数
# 实现 accuracy(predictions,labels)，等长空列表返回 None，长度不同抛 ValueError，其余返回准确率。打印 [1,0] 对 [1,1] 的结果。
# 预期程序输出：
# 0.5

def accuracy(predictions, labels):
    if len(predictions) != len(labels):
        raise ValueError("长度不一致")
    if not labels:
        return None
    correct = sum(pred == label for pred, label in zip(predictions, labels))
    return correct / len(labels)

print(accuracy([1, 0], [1, 1]))
