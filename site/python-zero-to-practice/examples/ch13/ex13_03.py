# 测试浮点结果
import math
result = 0.1 + 0.2
print(result == 0.3)
print(math.isclose(result, 0.3, rel_tol=1e-9, abs_tol=1e-12))
