# 星号解包
first, *middle, last = [1, 2, 3, 4]
print(first, middle, last)

def add(a, b):
    return a + b

print(add(*[2, 3]))
print(add(**{"a": 5, "b": 6}))
