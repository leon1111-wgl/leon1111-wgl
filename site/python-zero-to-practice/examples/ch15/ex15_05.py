# 带标注的函数
def average(values: list[float]) -> float | None:
    if not values:
        return None
    return sum(values) / len(values)

print(average([1.0, 3.0]))
print(average([]))
