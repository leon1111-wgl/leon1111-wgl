# 准确率与对齐
def accuracy(predictions, labels):
    if len(predictions) != len(labels):
        raise ValueError("长度不一致")
    if not labels:
        return None
    correct = sum(pred == label for pred, label in zip(predictions, labels))
    return correct / len(labels)

print(f"{accuracy([1, 0, 1, 1], [1, 1, 1, 0]):.1%}")
