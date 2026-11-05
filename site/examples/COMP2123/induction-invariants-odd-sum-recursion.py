# Leon | Original learning example
# A recursive function that follows its proof
# Python 3.12+ | Run: python induction-invariants-odd-sum-recursion.py
def sum_odd(n):
    """Return 1 + 3 + 5 + ... + (2n - 1), written in the shape of the proof."""
    if n == 0:
        return 0                          # base case: the empty sum
    return sum_odd(n - 1) + (2 * n - 1)   # step: trust n - 1, add the next odd number

for n in range(0, 7):
    value = sum_odd(n)
    print("n =", n, " sum =", value, " n*n =", n * n, " equal:", value == n * n)
