# 第 02_05 题 整箱装书
# 53 本书，每箱最多 12 本。输出完整箱数 4、剩余本数 5、实际需要箱数 5，每个一行。
# 预期程序输出：
# 4
# 5
# 5

books = 53
capacity = 12
print(books // capacity)
print(books % capacity)
print((books + capacity - 1) // capacity)
