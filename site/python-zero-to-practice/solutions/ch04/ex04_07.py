# 第 04_07 题 实验启动条件
# has_data=True，has_config=True，is_running=False。只有有数据、有配置且当前未运行时输出 可以启动，否则输出 暂不能启动。
# 预期程序输出：
# 可以启动

has_data = True
has_config = True
is_running = False
if has_data and has_config and not is_running:
    print("可以启动")
else:
    print("暂不能启动")
