# 默认参数与关键字
def greet(name, prefix="你好"):
    return f"{prefix}，{name}"

print(greet("小林"))
print(greet(prefix="晚上好", name="小陈"))
