# 第 13_04 题 保留坏行位置
# 实现 parse_numbers(lines)，返回 (values, bad_lines)，有效整数字符串进 values，解析失败的 1 起始行号进 bad_lines。打印对 ["1","x","3"] 的结果。
# 预期程序输出：
# ([1, 3], [2])

def parse_numbers(lines):
    values = []
    bad_lines = []
    for number, line in enumerate(lines, start=1):
        try:
            values.append(int(line))
        except ValueError:
            bad_lines.append(number)
    return values, bad_lines

print(parse_numbers(["1", "x", "3"]))
