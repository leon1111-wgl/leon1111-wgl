# 第 13_06 题 只捕获预期解析错误
# 实现 json_object(text)，JSON 解析失败或解析结果不是字典时返回 None，否则返回字典。分别打印对 {"a":1}、[]、bad 的结果。
# 预期程序输出：
# {'a': 1}
# None
# None

import json

def json_object(text):
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return None
    if not isinstance(data, dict):
        return None
    return data

print(json_object('{"a":1}'))
print(json_object('[]'))
print(json_object('bad'))
