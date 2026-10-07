# 第 09_06 题 无共享默认值
# 实现 append_new(value, items=None)，未传 items 时每次建立独立列表；传入列表时追加到该列表。依次打印 append_new("A") 与 append_new("B")。
# 预期程序输出：
# ['A']
# ['B']

def append_new(value, items=None):
    if items is None:
        items = []
    items.append(value)
    return items

print(append_new("A"))
print(append_new("B"))
