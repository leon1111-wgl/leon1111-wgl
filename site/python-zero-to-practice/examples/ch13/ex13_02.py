# 主动验证约定
def divide(total, count):
    if count <= 0:
        raise ValueError("count 必须为正数")
    return total / count

try:
    divide(10, 0)
except ValueError as error:
    print(error)
