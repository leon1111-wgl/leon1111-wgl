# Leon | Original learning example
# Recursion that needs strong induction
# Python 3.12+ | Run: python induction-invariants-power-strong-induction.py
def power(x, n):
    """Return (x ** n, number of multiplications used)."""
    if n == 0:
        return 1, 0                  # base case
    half, used = power(x, n // 2)    # a smaller call, but not n - 1
    result = half * half
    used += 1
    if n % 2 == 1:
        result = result * x
        used += 1
    return result, used

for n in [0, 1, 2, 5, 13, 64]:
    value, used = power(3, n)
    assert value == 3 ** n
    print("n =", n, " 3^n =", value, " multiplications:", used)
