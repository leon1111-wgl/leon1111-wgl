# 读取直到 q
total = 0
while True:
    text = input().strip()
    if text == "q":
        break
    total += int(text)
print(total)
