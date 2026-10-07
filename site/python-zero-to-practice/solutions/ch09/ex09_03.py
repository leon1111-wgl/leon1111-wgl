# 第 09_03 题 限制范围
# 实现 clamp(value, low, high)，假定 low<=high：低于 low 返回 low，高于 high 返回 high，否则原样返回。打印 clamp(120,0,100)。
# 预期程序输出：
# 100

def clamp(value, low, high):
    if value < low:
        return low
    if value > high:
        return high
    return value

print(clamp(120, 0, 100))
