// Leon | Original learning example
// Convert 202 by hand-style division and read ASCII codes
#include <stdio.h>

static char hex_digit(unsigned value) {
    return "0123456789ABCDEF"[value];
}

/* Turn n into binary by repeated division by 2, as you would on paper. */
static void show_division(unsigned n) {
    char digits[32];
    int count = 0;
    printf("convert %u\n", n);
    while (n > 0) {
        printf("  %u / 2 = %u remainder %u\n", n, n / 2, n % 2);
        digits[count++] = (char)('0' + n % 2);
        n /= 2;
    }
    printf("read the remainders from last to first: ");
    for (int i = count - 1; i >= 0; i--)
        putchar(digits[i]);
    putchar('\n');
}

/* Read a binary text left to right: double what you have, add the next bit. */
static unsigned from_binary(const char *text) {
    unsigned value = 0;
    for (; *text != '\0'; text++)
        value = value * 2 + (unsigned)(*text - '0');
    return value;
}

int main(void) {
    show_division(202);

    printf("group by four bits:");
    for (int shift = 4; shift >= 0; shift -= 4) {
        unsigned nibble = (202u >> shift) & 0xFu;
        printf(" ");
        for (int bit = 3; bit >= 0; bit--)
            putchar((nibble >> bit) & 1u ? '1' : '0');
        printf("=%c", hex_digit(nibble));
    }
    printf("\nso 202 is 0x%X\n", 202u);
    printf("back to decimal: 11001010 -> %u\n", from_binary("11001010"));

    char upper = 'K';
    char lower = 'k';
    printf("'%c' = %d = 0x%X\n", upper, upper, (unsigned)upper);
    printf("'%c' = %d = 0x%X\n", lower, lower, (unsigned)lower);
    printf("difference = %d, so clearing bit 5 turns '%c' into '%c'\n",
           lower - upper, lower, (char)(lower & ~0x20));
    char digit = '7';
    printf("'%c' = %d, and '%c' - '0' = %d\n", digit, digit, digit, digit - '0');
    return 0;
}
