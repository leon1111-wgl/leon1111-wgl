# 遇到目标就停止
for value in [4, 8, 15, 16]:
    if value > 10:
        print("首个大于 10 的数", value)
        break
    print("检查过", value)
