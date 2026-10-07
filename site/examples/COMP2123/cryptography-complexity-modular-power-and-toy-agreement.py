# Leon | Original learning example
# Compute powers by repeated squaring
# Python 3.12+ | Run: python cryptography-complexity-modular-power-and-toy-agreement.py
def power_mod(base, exponent, modulus):
    result = 1
    base %= modulus
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent //= 2
    return result
modulus, generator = 23, 5
a, b = 3, 4
public_a = power_mod(generator, a, modulus)
public_b = power_mod(generator, b, modulus)
shared_a = power_mod(public_b, a, modulus)
shared_b = power_mod(public_a, b, modulus)
print("public:", public_a, public_b)
print("shared:", shared_a, shared_b)
for guess in range(22):
    if power_mod(generator, guess, modulus) == public_a:
        print("recovered a:", guess)
        break
