# 第 13_09 题 AI / Agent：逐行检查工具日志并记录错误
# 实现 read_tool_log(text)，输入保证是字符串。每个非空行应为 JSON 对象，tool 为非空字符串，ok 为 bool。跳过空行；合法记录将 tool.strip() 后保存为只含 tool、ok 的新字典。返回 (records, errors)，errors 每项为 {"line":原始行号,"kind":类别}；坏 JSON 类别为 json，非字典/缺字段/类型错误为 schema，tool 仅空白为 value。每行最多报一个错误，按上述顺序检查。五行依次为 {"tool":" search ","ok":true}、空行、bad-json、{"tool":"count","ok":1}、{"tool":"save","ok":false}。最后打印 records 和 errors，各占一行。
# 预期程序输出：
# [{'tool': 'search', 'ok': True}, {'tool': 'save', 'ok': False}]
# [{'line': 3, 'kind': 'json'}, {'line': 4, 'kind': 'schema'}]

# 请在下面独立作答。先保存，再运行。
