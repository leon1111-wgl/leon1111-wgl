# 第 13_01 题 容错转整数
# 实现 parse_int(text)，转换成功返回整数，ValueError 时返回 None。依次打印对 "12" 和 "abc" 的结果。输入约定为字符串。
# 预期程序输出：
# 12
# None

def parse_int(text):
    try:
        return int(text)
    except ValueError:
        return None

print(parse_int("12"))
print(parse_int("abc"))
