# 文本清理：工具标签为什么越删越多
raw = "  tool:lookup  "
cleaned = raw.strip()
wrong = cleaned.lstrip("tool:")
name = cleaned.removeprefix("tool:")
print(repr(raw))
print(repr(cleaned))
print(repr(wrong))
print(repr(name))

filename = "report.txt"
print(repr(filename.rstrip(".txt")))
print(repr(filename.removesuffix(".txt")))
