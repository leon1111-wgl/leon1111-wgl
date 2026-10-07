# 第 08_01 题 库存更新
# stock = {"apple":3,"pear":2}，苹果补货 5 个，新增 banana 4 个，输出 stock 的 Python 表示。
# 预期程序输出：
# {'apple': 8, 'pear': 2, 'banana': 4}

stock = {"apple": 3, "pear": 2}
stock["apple"] += 5
stock["banana"] = 4
print(stock)
