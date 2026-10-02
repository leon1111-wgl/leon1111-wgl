# Guoliang | Original learning example
# See an array insertion shift values
# Python 3.12+ | Run: python lists-representations-array-insert-shifts.py
items = ["L", "M", "N", "P"]
position = 1
items.append(None)
shifts = 0
for i in range(len(items) - 1, position, -1):
    items[i] = items[i - 1]
    shifts += 1
items[position] = "X"
print(items)
print("shifts:", shifts)
