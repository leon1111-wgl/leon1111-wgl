# 第 12_01 题 提取非空行
# 实现 nonempty_lines(text)，去各行两端空白，丢弃空行。打印对 " A \n\n B " 的结果。
# 预期程序输出：
# ['A', 'B']

def nonempty_lines(text):
    result = []
    for line in text.splitlines():
        clean = line.strip()
        if clean:
            result.append(clean)
    return result

print(nonempty_lines(" A \n\n B "))
