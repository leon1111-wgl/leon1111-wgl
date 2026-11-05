# 第 09_11 题 AI / Agent：将更早历史与最近消息分开
# 实现 split_history(messages, keep)。messages 是按从旧到新排列的字符串列表；keep 保证为非负整数，不使用 bool。返回 (older, recent)：recent 是最后至多 keep 条且顺序不变，older 是前面的其余消息。keep=0 时 recent=[]、older 包含全部；keep 超过长度时 older=[]、recent 包含全部。两个返回值每次都是新的外层列表，不修改输入，也不在函数内打印。打印对 ["问候", "提问", "检索", "回答"] 分别取 keep=2 与 keep=0 的返回值。
# 预期程序输出：
# (['问候', '提问'], ['检索', '回答'])
# (['问候', '提问', '检索', '回答'], [])

# 请在下面独立作答。先保存，再运行。
