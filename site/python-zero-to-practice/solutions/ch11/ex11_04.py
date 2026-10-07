# 第 11_04 题 十进制精确相加
# 用 decimal.Decimal 从字符串构造 0.1 和 0.2，相加并输出 0.3。
# 预期程序输出：
# 0.3

from decimal import Decimal
print(Decimal("0.1") + Decimal("0.2"))
