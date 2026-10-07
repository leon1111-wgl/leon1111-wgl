# 全部与至少一个
scores = [50, 80, 90]
print(any(score >= 60 for score in scores))
print(all(score >= 60 for score in scores))
print(any([]), all([]))
