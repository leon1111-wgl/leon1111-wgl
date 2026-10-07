# 按类别累计
records = [("书", 30), ("餐饮", 20), ("书", 50)]
totals = {}
for category, amount in records:
    totals[category] = totals.get(category, 0) + amount
print(totals)
