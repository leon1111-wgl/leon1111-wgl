# 过滤与替换
numbers = [-2, 0, 3]
print([x for x in numbers if x > 0])
print([x if x > 0 else 0 for x in numbers])
