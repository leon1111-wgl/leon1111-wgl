# 成绩等级
score = 85
if not 0 <= score <= 100:
    print("成绩无效")
elif score >= 90:
    print("优秀")
elif score >= 60:
    print("通过")
else:
    print("待加强")
