# 第 08_05 题 两班共同选课
# a={"python","math"}，b={"python","english"}，输出共同课程的排序列表 ["python"]。
# 预期程序输出：
# ['python']

a = {"python", "math"}
b = {"python", "english"}
print(sorted(a & b))
