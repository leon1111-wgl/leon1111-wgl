# 提前返回处理空输入
def mean(values):
    if not values:
        return None
    return sum(values) / len(values)

print(mean([80, 100]))
print(mean([]))
