# 读取与默认值
student = {"name": "小林", "score": 85}
student["score"] = 90
print(student["name"], student["score"])
print(student.get("city", "未知"))
print("city" in student)
