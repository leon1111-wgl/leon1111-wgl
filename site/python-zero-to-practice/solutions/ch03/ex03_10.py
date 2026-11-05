# 第 03_10 题 工具记录名：按约定清理两端
# raw = "  tool:lookup.txt  "。约定按顺序执行：去掉两端空白，保存为 cleaned；只去掉开头一次完整 tool:，保存为 without_prefix；只去掉结尾一次完整 .txt，保存为 name。大小写必须相符，未匹配到的标记与内部内容保留，不增加第二次空白清理。依次输出 repr(cleaned)、repr(without_prefix)、repr(name)、repr(raw)，各占一行。只用字符串、赋值、方法调用和 print，不写函数。本题练习文本变换，不检查工具名是否可用。
# 预期程序输出：
# 'tool:lookup.txt'
# 'lookup.txt'
# 'lookup'
# '  tool:lookup.txt  '

raw = "  tool:lookup.txt  "
cleaned = raw.strip()
without_prefix = cleaned.removeprefix("tool:")
name = without_prefix.removesuffix(".txt")
print(repr(cleaned))
print(repr(without_prefix))
print(repr(name))
print(repr(raw))
