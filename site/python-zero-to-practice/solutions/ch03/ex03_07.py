# 第 03_07 题 确认是否已保存清洗结果
# text="  Python  "。有人调用 text.strip() 后直接打印 text。请修复并输出 Python，再输出长度 6。
# 预期程序输出：
# Python
# 6

text = "  Python  "
text = text.strip()
print(text)
print(len(text))
