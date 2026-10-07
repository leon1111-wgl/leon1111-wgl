# 第 13_05 题 防止空字符串输入
# 实现 require_name(text)，strip 后为空则抛 ValueError，否则返回清理后的姓名。打印对 " A " 的结果。
# 预期程序输出：
# A

def require_name(text):
    name = text.strip()
    if not name:
        raise ValueError("姓名不能为空")
    return name

print(require_name(" A "))
