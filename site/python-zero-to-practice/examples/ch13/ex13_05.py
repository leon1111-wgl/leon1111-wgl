# 带行号记录坏数据
lines = ["80", "oops", "90"]
for line_number, text in enumerate(lines, start=1):
    try:
        score = int(text)
    except ValueError:
        print(f"第 {line_number} 行不是整数：{text}")
        continue
    if not 0 <= score <= 100:
        print(f"第 {line_number} 行超出范围")
        continue
    print("保留", score)
