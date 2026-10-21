# AI / Agent：列表保存顺序，字典保存消息字段
messages = [
    {"role": "user", "content": "什么是列表？"},
    {"role": "assistant", "content": "列表保存有顺序的元素。"},
]
messages.append({"role": "user", "content": "给我一个例子。"})
for message in messages:
    print(f"{message['role']}: {message['content']}")
print(len(messages))
