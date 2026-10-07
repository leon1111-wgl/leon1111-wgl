# 保序去重与 seen
seen = set()
unique = []
for word in ["a", "b", "a", "c"]:
    if word not in seen:
        seen.add(word)
        unique.append(word)
print(unique)
