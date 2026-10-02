# Guoliang | Original learning example
# Count divisibility tests and input bits
# Python 3.12+ | Run: python cryptography-complexity-trial-division-bit-length.py
from math import isqrt
def trial_factor(number):
    checks = 0
    for divisor in range(2, isqrt(number) + 1):
        checks += 1
        if number % divisor == 0:
            return divisor, checks
    return None, checks
for number in [221, 257]:
    factor, checks = trial_factor(number)
    print("number:", number, "bits:", number.bit_length(), "factor:", factor, "checks:", checks)
