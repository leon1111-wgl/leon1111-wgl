# 第 12_07 题 AI / Agent：读回合法的 JSONL 消息
# 实现 parse_messages(text)：输入为多行文本，每个非空行保证是含 role、content 的合法 JSON 对象；跳过空行，返回解析后的字典列表。调用文本为两行 {"role":"user","content":"hi"} 与 {"role":"assistant","content":"hello"}，中间有一空行。输出列表长度和第二条正文。
# 预期程序输出：
# 2
# hello

import json

def parse_messages(text):
    messages = []
    for line in text.splitlines():
        if not line.strip():
            continue
        messages.append(json.loads(line))
    return messages

text = '{"role":"user","content":"hi"}\n\n{"role":"assistant","content":"hello"}'
messages = parse_messages(text)
print(len(messages))
print(messages[1]["content"])
