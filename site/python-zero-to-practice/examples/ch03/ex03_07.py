# 切片追踪：同样倒着走，为何有时为空
s = "KLMNOP"
print(repr(s[1:5:2]))
print(repr(s[4:1:-1]))
print(repr(s[1:4:-1]))
print(repr(s[5:0:-1]))
print(repr(s[5::-1]))
print(repr(s[5:-1:-1]))
