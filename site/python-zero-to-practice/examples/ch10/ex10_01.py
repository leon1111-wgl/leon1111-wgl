# 循环与推导式等价
numbers = [-2, 0, 3, 4]
result = []
for number in numbers:
    if number > 0:
        result.append(number ** 2)
print(result)
print([number ** 2 for number in numbers if number > 0])
