# AI / Agent：返回的新轮数要由调用者接住
def next_round(current):
    return current + 1

rounds = 0
for _ in range(3):
    next_round(rounds)
print(f"未接收：{rounds}")

for _ in range(3):
    rounds = next_round(rounds)
    print(f"保存后：{rounds}")
