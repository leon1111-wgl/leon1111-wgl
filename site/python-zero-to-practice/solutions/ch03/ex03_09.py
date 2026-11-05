# 第 03_09 题 设备短码：先取一段，再反转
# 给定 code = "Q7M2R8"。保存 tail 为最后 3 个字符，head 为前 3 个字符。依次输出 tail、tail 的倒序、head 的倒序，每项一行。最后输出 repr(code[2:-1:-1])，并解释为何它不是前 3 个字符的倒序。本题只用字符串、赋值、切片和 print，不写函数。
# 预期程序输出：
# 2R8
# 8R2
# M7Q
# ''

code = "Q7M2R8"
tail = code[-3:]
head = code[:3]
print(tail)
print(tail[::-1])
print(head[::-1])
print(repr(code[2:-1:-1]))
