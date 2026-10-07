# 小型回归检查
def clamp(value, low, high):
    return min(max(value, low), high)

assert clamp(-1, 0, 10) == 0
assert clamp(5, 0, 10) == 5
assert clamp(11, 0, 10) == 10
print("3 个检查通过")
