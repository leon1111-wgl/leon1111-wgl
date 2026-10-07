# 收集可变参数
def describe(*args, **kwargs):
    print(args)
    print(kwargs)

describe("A", "B", score=90)
