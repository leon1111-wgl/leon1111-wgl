# 第 08_09 题 AI / Agent：统计用户消息
# messages 为 [{"role": "user", "content": "hi"}, {"role": "assistant", "content": "hello"}, {"role": "user", "content": "bye"}]。只输出用户消息正文，并在最后输出用户消息数。所有记录都保证有这两个键。
# 预期程序输出：
# hi
# bye
# 2

messages = [
    {"role": "user", "content": "hi"},
    {"role": "assistant", "content": "hello"},
    {"role": "user", "content": "bye"},
]
count = 0
for message in messages:
    if message["role"] == "user":
        print(message["content"])
        count += 1
print(count)
