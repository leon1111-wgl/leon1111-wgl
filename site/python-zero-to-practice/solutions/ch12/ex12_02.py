# 第 12_02 题 配置解析
# 实现 read_batch_size(text)，解析 JSON 字符串并读取 batch_size，缺失默认 8。打印对 {"name":"demo"} 的结果。假定输入 JSON 对象合法。
# 预期程序输出：
# 8

import json

def read_batch_size(text):
    config = json.loads(text)
    return config.get("batch_size", 8)

print(read_batch_size('{"name":"demo"}'))
