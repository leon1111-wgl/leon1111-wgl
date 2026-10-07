# 生成器暂停
def countdown(start):
    while start > 0:
        yield start
        start -= 1

numbers = countdown(3)
print(next(numbers))
print(list(numbers))
