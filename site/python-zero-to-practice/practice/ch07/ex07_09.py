# 第 07_09 题 Agent 候选请求：分到两份新列表
# allowed = ["search", "count"]，requests = ["search", "skip", "skip", "count", "search"]，输入保证为字符串列表。用普通 for 和 if/else，把名称在 allowed 中的请求追加到新列表 accepted，其余追加到另一个新列表 rejected。精确匹配，区分大小写，不清理空白；每组保持原有相对顺序和重复次数，不修改 allowed 或 requests，不执行工具。依次打印 accepted、rejected、requests，各占一行。不写函数、集合或推导式。
# 预期程序输出：
# ['search', 'count', 'search']
# ['skip', 'skip']
# ['search', 'skip', 'skip', 'count', 'search']

# 请在下面独立作答。先保存，再运行。
