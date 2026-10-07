# 无命中的处理
found = False
for value in [1, 3, 5]:
    if value % 2 == 0:
        found = True
        print(value)
        break
if not found:
    print("没有偶数")
