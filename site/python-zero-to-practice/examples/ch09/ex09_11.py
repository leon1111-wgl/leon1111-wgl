# AI / Agent：最近消息的零条边界
def latest_messages(messages, keep):
    if keep == 0:
        return []
    return messages[-keep:]

messages = ["先读题", "列步骤", "做检查"]
for keep in [2, 0, 5]:
    print("keep =", keep)
    print("直接切片：", messages[-keep:])
    print("按约定选择：", latest_messages(messages, keep))
print("原消息：", messages)
