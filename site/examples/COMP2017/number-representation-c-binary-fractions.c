// Leon | Original learning example
// Why 0.1 is not exact in binary
#include <stdio.h>
#include <stdint.h>
#include <string.h>

static unsigned gcd(unsigned a, unsigned b) {
    while (b != 0) {
        unsigned r = a % b;
        a = b;
        b = r;
    }
    return a;
}

/* A fraction ends in binary exactly when its reduced denominator is a power of two. */
static int ends_in_binary(unsigned p, unsigned q) {
    q /= gcd(p, q);
    return (q & (q - 1)) == 0;
}

/* Produce binary digits of num/den by doubling the remainder, like long division. */
static void expand(unsigned num, unsigned den, int digits) {
    printf("%u/%u in binary: 0.", num, den);
    unsigned remainder = num;
    for (int i = 0; i < digits && remainder != 0; i++) {
        remainder *= 2;
        putchar(remainder >= den ? '1' : '0');
        if (remainder >= den)
            remainder -= den;
    }
    printf("%s\n", remainder == 0 ? "  (stops)" : "...  (keeps going)");
}

int main(void) {
    static const unsigned tests[][2] = {{3, 4}, {7, 8}, {1, 10}, {1, 5}, {1, 3}};
    for (size_t i = 0; i < sizeof tests / sizeof tests[0]; i++)
        printf("%u/%u ends in binary: %s\n", tests[i][0], tests[i][1],
               ends_in_binary(tests[i][0], tests[i][1]) ? "yes" : "no");

    expand(3, 4, 12);
    expand(1, 10, 16);

    printf("remainders for 1/10 while doubling:");
    unsigned r = 1;
    for (int i = 0; i < 9; i++) {
        printf(" %u", r);
        r = (r * 2) % 10;
    }
    printf("\n");

    double tenth = 0.1;
    uint64_t bits;
    memcpy(&bits, &tenth, sizeof bits);
    printf("0.1 as a double: 0x%016llX\n", (unsigned long long)bits);
    printf("exponent field %llu, stored mantissa 0x%013llX\n",
           (unsigned long long)((bits >> 52) & 0x7FF),
           (unsigned long long)(bits & 0xFFFFFFFFFFFFFull));

    double sum = 0.1 + 0.2;
    double diff = sum - 0.3;
    if (diff < 0)
        diff = -diff;
    printf("0.1 + 0.2 == 0.3 ? %s\n", sum == 0.3 ? "yes" : "no");
    printf("within 1e-9 of 0.3 ? %s\n", diff < 1e-9 ? "yes" : "no");
    printf("%.17g\n", sum);
    printf("10 + 20 cents == 30 cents ? %s\n", 10 + 20 == 30 ? "yes" : "no");
    return 0;
}
