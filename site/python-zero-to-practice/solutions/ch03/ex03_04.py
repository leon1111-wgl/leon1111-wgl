# 第 03_04 题 清理多余空格
# 把 "  I   love  Python  " 转成单个空格分隔的 "I love Python"。
# 预期程序输出：
# I love Python

text = "  I   love  Python  "
print(" ".join(text.split()))
