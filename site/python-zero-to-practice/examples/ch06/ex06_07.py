# AI / Agent：最多执行三轮的任务循环
step = 0
max_steps = 3
finished = False
while step < max_steps:
    step += 1
    print(f"第 {step} 轮")
    if step == 2:
        finished = True
        break
print(f"已完成：{finished}")
print(f"实际轮数：{step}")
