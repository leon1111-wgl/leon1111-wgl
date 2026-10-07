# 第 04_02 题 运费规则
# 订单金额 99 元，满 100 元免运费，否则运费 8 元。输出应付总额 107。
# 预期程序输出：
# 107

amount = 99
if amount >= 100:
    shipping = 0
else:
    shipping = 8
print(amount + shipping)
