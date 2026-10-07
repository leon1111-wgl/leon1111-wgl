# 第 16_05 题 补齐批次
# 实现 pad_batch(sequences,pad_id=0)，返回 (padded,masks)，补到本批最大长度，空批返回 ([],[])，不修改输入。打印 [[2,3],[4]] 的结果。
# 预期程序输出：
# ([[2, 3], [4, 0]], [[1, 1], [1, 0]])

def pad_batch(sequences, pad_id=0):
    if not sequences:
        return [], []
    width = max(len(sequence) for sequence in sequences)
    padded = []
    masks = []
    for sequence in sequences:
        extra = width - len(sequence)
        padded.append(sequence + [pad_id] * extra)
        masks.append([1] * len(sequence) + [0] * extra)
    return padded, masks

print(pad_batch([[2, 3], [4]]))
