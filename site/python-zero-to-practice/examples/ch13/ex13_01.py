# 具体捕获转换错误
texts = ["10", "bad", "20"]
values = []
for text in texts:
    try:
        value = int(text)
    except ValueError:
        print("跳过无效值", repr(text))
    else:
        values.append(value)
print(sum(values))
