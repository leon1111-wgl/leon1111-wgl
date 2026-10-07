# 清洗并保序去重
raw = ["  Hello   Python ", "", "hello python", "Learn AI"]
seen = set()
cleaned = []
for text in raw:
    clean = " ".join(text.lower().split())
    if clean and clean not in seen:
        seen.add(clean)
        cleaned.append(clean)
print(cleaned)
