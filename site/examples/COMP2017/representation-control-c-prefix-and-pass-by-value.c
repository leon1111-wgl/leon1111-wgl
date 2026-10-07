// Leon | Original learning example
// Trace a prefix sum and a copied parameter
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>

static int replace_copy(int value) {
    value = 9;
    return value;
}
int main(void) {
    int values[] = {2, 4, 7};
    int sum = 0;
    size_t count = sizeof values / sizeof values[0];
    for (size_t i = 0; i < count; i++) {
        sum += values[i];
        printf("processed=%zu sum=%d\n", i + 1, sum);
    }
    int original = 5;
    printf("returned=%d\n", replace_copy(original));
    printf("caller=%d\n", original);
    return 0;
}
