# 第 03_05 题 切片推理
# 给定 s = "abcdef"，依次输出 bdf、fedcba、abc，各一行。
# 预期程序输出：
# bdf
# fedcba
# abc

s = "abcdef"
print(s[1::2])
print(s[::-1])
print(s[:3])
