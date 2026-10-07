# 补齐与掩码
sequences = [[2, 3, 4], [2]]
width = max(len(sequence) for sequence in sequences)
padded = []
masks = []
for sequence in sequences:
    padding = width - len(sequence)
    padded.append(sequence + [0] * padding)
    masks.append([1] * len(sequence) + [0] * padding)
print(padded)
print(masks)
