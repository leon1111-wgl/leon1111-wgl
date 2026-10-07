# 默认列表陷阱与修复
def bad_add(value, items=[]):
    items.append(value)
    return items

print(bad_add("A"))
print(bad_add("B"))

def good_add(value, items=None):
    if items is None:
        items = []
    items.append(value)
    return items

print(good_add("A"))
print(good_add("B"))
