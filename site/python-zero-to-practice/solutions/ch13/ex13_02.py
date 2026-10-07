# 第 13_02 题 分数合法性
# 实现 valid_score(text)，字符串可转整数且在 0—100 内返回该整数，否则返回 None。打印对 "101" 和 "60" 的结果。
# 预期程序输出：
# None
# 60

def valid_score(text):
    try:
        value = int(text)
    except ValueError:
        return None
    if not 0 <= value <= 100:
        return None
    return value

print(valid_score("101"))
print(valid_score("60"))
