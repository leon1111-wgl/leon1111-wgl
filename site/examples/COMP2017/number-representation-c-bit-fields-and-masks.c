// Leon | Original learning example
// Pack a date with a bit-field and with shifts
#include <stdio.h>

/* Three small numbers share 7 + 4 + 5 = 16 bits. */
struct PackedDate {
    unsigned year : 7;   /* years since 1980, 0..127 */
    unsigned month : 4;  /* 0..15, we use 1..12 */
    unsigned day : 5;    /* 0..31, we use 1..31 */
};

/* Exact layout chosen by us, with shifts and masks:
   bits 15..9 year, bits 8..5 month, bits 4..0 day. */
static unsigned pack(unsigned year, unsigned month, unsigned day) {
    return (year << 9) | (month << 5) | day;
}

static void print_bits16(unsigned word) {
    for (int bit = 15; bit >= 0; bit--) {
        putchar((word >> bit) & 1u ? '1' : '0');
        if (bit % 4 == 0 && bit != 0)
            putchar(' ');
    }
}

int main(void) {
    struct PackedDate date;
    date.year = 45;
    date.month = 11;
    date.day = 5;
    printf("bit-field read back: year=%u month=%u day=%u\n", date.year, date.month, date.day);

    unsigned word = pack(45, 11, 5);
    printf("packed word: 0x%04X = ", word);
    print_bits16(word);
    printf("\n");

    unsigned year = (word >> 9) & 0x7Fu;
    unsigned month = (word >> 5) & 0xFu;
    unsigned day = word & 0x1Fu;
    printf("unpacked with masks: year=%u month=%u day=%u\n", year, month, day);

    unsigned too_big = 17;
    date.month = too_big;
    printf("stored 17 in a 4-bit field, read back %u\n", date.month);

    unsigned flags = 0;
    flags |= 1u << 2;
    flags |= 1u << 0;
    printf("flags after setting bits 2 and 0: %u\n", flags);
    printf("bit 1 set? %s\n", (flags & (1u << 1)) ? "yes" : "no");
    flags &= ~(1u << 2);
    printf("flags after clearing bit 2: %u\n", flags);
    flags ^= 1u << 3;
    printf("flags after toggling bit 3: %u\n", flags);
    return 0;
}
