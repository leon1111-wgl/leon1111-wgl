# Guoliang | Original learning example
# Multiply using three recursive products
# Python 3.12+ | Run: python karatsuba-master-karatsuba-three-products.py
def karatsuba(x, y):
    if x < 10 or y < 10:
        return x * y
    digits = max(len(str(x)), len(str(y)))
    base = 10 ** (digits // 2)
    high_x, low_x = divmod(x, base)
    high_y, low_y = divmod(y, base)
    high_product = karatsuba(high_x, high_y)
    low_product = karatsuba(low_x, low_y)
    combined = karatsuba(high_x + low_x, high_y + low_y)
    cross = combined - high_product - low_product
    return high_product * base * base + cross * base + low_product
print(karatsuba(23, 47))
print(karatsuba(1234, 5678))
print(karatsuba(0, 900))
