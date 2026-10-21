# 第 14_05 题 AI / Agent：有条数上限的会话记忆
# 实现 RecentMessages(limit)。limit 必须为大于 0 的 int，bool 不接受，否则 raise ValueError。每个实例有自己的 messages 列表；add(text) 只接受字符串，添加后保留最后 limit 条，返回当前条数。用 limit=2 依次添加 "a"、"b"、"c"，打印 messages。
# 预期程序输出：
# ['b', 'c']

class RecentMessages:
    def __init__(self, limit):
        if type(limit) is not int or limit <= 0:
            raise ValueError("limit 必须为正整数")
        self.limit = limit
        self.messages = []

    def add(self, text):
        if not isinstance(text, str):
            raise ValueError("text 必须为字符串")
        self.messages.append(text)
        self.messages = self.messages[-self.limit:]
        return len(self.messages)

session = RecentMessages(2)
session.add("a")
session.add("b")
session.add("c")
print(session.messages)
