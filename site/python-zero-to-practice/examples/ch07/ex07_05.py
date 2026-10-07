# 浅拷贝的边界
import copy
a = [[1], [2]]
b = a.copy()
c = copy.deepcopy(a)
b[0].append(9)
print(a)
print(b)
print(c)
