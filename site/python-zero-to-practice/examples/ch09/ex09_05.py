# 作用域与返回
score = 60

def improve(value):
    value = value + 10
    return value

new_score = improve(score)
print(score, new_score)
