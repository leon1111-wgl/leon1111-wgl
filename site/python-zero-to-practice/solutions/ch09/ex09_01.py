# 第 09_01 题 温度转换函数
# 实现 to_fahrenheit(celsius)，返回摄氏转华氏的值。展示 print(to_fahrenheit(25)) 输出 77.0。
# 预期程序输出：
# 77.0

def to_fahrenheit(celsius):
    return celsius * 9 / 5 + 32

print(to_fahrenheit(25))
