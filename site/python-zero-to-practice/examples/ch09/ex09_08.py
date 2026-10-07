# 多个结果与文档字符串
def summarize(values):
    """返回数值列表的总和与项数。"""
    return sum(values), len(values)

total, count = summarize([2, 4, 6])
print(total, count)
