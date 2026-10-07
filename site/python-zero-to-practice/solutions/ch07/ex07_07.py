# 第 07_07 题 修复 sort 赋值
# values=[3,1,2]。修复 values=values.sort() 导致 None 的问题；要求保留 values 的列表并输出升序。
# 预期程序输出：
# [1, 2, 3]

values = [3, 1, 2]
values.sort()
print(values)
