# 记录列表
students = [
    {"name": "A", "score": 55},
    {"name": "B", "score": 80},
]
for student in students:
    if student["score"] >= 60:
        print(student["name"])
