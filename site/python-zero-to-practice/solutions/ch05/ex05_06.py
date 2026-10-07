# 第 05_06 题 统计元音
# 统计 "Education" 中英文字母元音 a e i o u 的数量，忽略大小写，输出 5。
# 预期程序输出：
# 5

count = 0
for char in "Education".lower():
    if char in "aeiou":
        count += 1
print(count)
