# 词频统计
counts = {}
for word in "python is fun python is useful".split():
    counts[word] = counts.get(word, 0) + 1
for word, count in counts.items():
    print(word, count)
