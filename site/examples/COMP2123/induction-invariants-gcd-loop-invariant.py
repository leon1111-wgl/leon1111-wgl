# Leon | Original learning example
# A loop whose invariant never changes
# Python 3.12+ | Run: python induction-invariants-gcd-loop-invariant.py
def common_divisors(a, b):
    """Brute-force checker: every d >= 1 that divides both a and b."""
    return [d for d in range(1, max(a, b) + 1) if a % d == 0 and b % d == 0]

a, b = 252, 105
original = common_divisors(a, b)
print("start  a =", a, " b =", b, " common divisors:", original)

while b != 0:
    old_b = b
    a, b = b, a % b
    assert common_divisors(a, b) == original    # invariant is maintained
    assert 0 <= b < old_b                       # b shrinks, so the loop must end
    print("after  a =", a, " b =", b, " common divisors:", common_divisors(a, b))

print("exit: b = 0, so the greatest common divisor is a =", a)
