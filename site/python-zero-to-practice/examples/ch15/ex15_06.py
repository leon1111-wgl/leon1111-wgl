# AI / Agent：用生成器模拟逐段到达的文字
def simulated_stream():
    yield "先学"
    yield " Python"
    yield "，再做项目。"

pieces = []
stream = simulated_stream()
for piece in stream:
    pieces.append(piece)
    print(f"收到：{piece}")
print("完整：" + "".join(pieces))
print(list(stream))
