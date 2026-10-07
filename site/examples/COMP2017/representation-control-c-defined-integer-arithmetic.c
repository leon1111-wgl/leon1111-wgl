// Leon | Original learning example
// Observe defined wrap and guard signed addition
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

int main(void) {
    unsigned int largest = UINT_MAX;
    printf("unsigned wrap=%u\n", largest + 1u);
    int value = INT_MAX;
    if (value > INT_MAX - 1)
        puts("signed addition rejected");
    else
        printf("signed sum=%d\n", value + 1);
    printf("integer quotient=%d\n", 13 / 3);
    printf("floating quotient=%.4f\n", 13.0 / 3.0);
    return 0;
}
