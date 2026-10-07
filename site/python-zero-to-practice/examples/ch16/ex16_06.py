# 二维形状检查
rows = [[1, 2], [3, 4], [5, 6]]
width = len(rows[0]) if rows else 0
is_rectangular = all(len(row) == width for row in rows)
print(len(rows), width)
print(is_rectangular)
