# 第 04_03 题 合法分数
# score = 105。若不在 0 到 100 内输出 无效，否则达到 60 输出 通过，未达到输出 未通过。
# 预期程序输出：
# 无效

score = 105
if not 0 <= score <= 100:
    print("无效")
elif score >= 60:
    print("通过")
else:
    print("未通过")
