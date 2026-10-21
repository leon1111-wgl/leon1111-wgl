# AI / Agent：两个会话不能共用消息列表
class ChatSession:
    def __init__(self, name):
        self.name = name
        self.messages = []

    def add(self, text):
        self.messages.append(text)
        return len(self.messages)

alice = ChatSession("Alice")
bob = ChatSession("Bob")
count = alice.add("我在学习 Python")
print(alice.name, count)
print(bob.name, len(bob.messages))
print(alice.messages is bob.messages)
