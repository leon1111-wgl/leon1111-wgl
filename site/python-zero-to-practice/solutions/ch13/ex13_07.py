# 第 13_07 题 AI / Agent：验证工具调用数据
# 实现 read_call(text)：解析 JSON，要求最外层为字典、name 恰好为 "char_count"、arguments 为字典且其中 text 为字符串。成功时返回 arguments["text"]；不满足任一条件时 raise ValueError。空字符串允许。调用 {"name":"char_count","arguments":{"text":"Python"}} 并打印返回文本。
# 预期程序输出：
# Python

import json

def read_call(text):
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("调用必须是对象")
    if data.get("name") != "char_count":
        raise ValueError("不支持的工具名")
    arguments = data.get("arguments")
    if not isinstance(arguments, dict):
        raise ValueError("arguments 必须是对象")
    content = arguments.get("text")
    if not isinstance(content, str):
        raise ValueError("text 必须是字符串")
    return content

request = '{"name":"char_count","arguments":{"text":"Python"}}'
print(read_call(request))
