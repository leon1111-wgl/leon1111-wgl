# Leon | Original learning example
# See the four products Karatsuba avoids
# Python 3.12+ | Run: python karatsuba-master-schoolbook-digit-products.py
x, y = 23, 47
high_x, low_x = divmod(x, 10)
high_y, low_y = divmod(y, 10)
parts = [("high-high", high_x * high_y, 100),
         ("high-low", high_x * low_y, 10),
         ("low-high", low_x * high_y, 10),
         ("low-low", low_x * low_y, 1)]
result = 0
for name, product, place in parts:
    result += product * place
    print(name, product, "place:", place, "running:", result)
print("product:", result)
print("ordinary leaves at depth 3:", 4 ** 3)
print("Karatsuba leaves at depth 3:", 3 ** 3)
