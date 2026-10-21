# 作用域排错：先复现，再用参数和返回值修复
rounds = 0

def broken_round():
    rounds += 1
    return rounds

try:
    broken_round()
except UnboundLocalError as error:
    print(type(error).__name__)
print(f"外部轮数：{rounds}")

def fixed_round(current):
    return current + 1

rounds = fixed_round(rounds)
rounds = fixed_round(rounds)
print(f"修复后：{rounds}")
