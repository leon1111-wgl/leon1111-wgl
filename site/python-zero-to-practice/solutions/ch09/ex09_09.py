# 第 09_09 题 AI / Agent：先约定工具的输入和返回结构
# 实现 summarize_text(text)，输入保证是字符串。先 strip；返回字典，字段 chars 为清理后的长度、preview 为前 4 个字符、empty 表示是否为空。函数不能打印。用 "  Python  " 调用，依次打印三个字段。
# 预期程序输出：
# 6
# Pyth
# False

def summarize_text(text):
    cleaned = text.strip()
    return {
        "chars": len(cleaned),
        "preview": cleaned[:4],
        "empty": cleaned == "",
    }

result = summarize_text("  Python  ")
print(result["chars"])
print(result["preview"])
print(result["empty"])
