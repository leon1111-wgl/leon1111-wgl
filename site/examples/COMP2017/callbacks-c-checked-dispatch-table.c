// Guoliang | Original learning example
// Select behavior through a checked table
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>

typedef int (*Operation)(int, int);
static int sum(int a, int b) {
    return a + b;
}
static int difference(int a, int b) {
    return a - b;
}
int main(void) {
    Operation operations[] = {sum, difference};
    size_t count = sizeof operations / sizeof operations[0];
    for (size_t index = 0; index <= count; index++) {
        if (index >= count) {
            puts("invalid operation");
            continue;
        }
        printf("operation %zu=%d\n", index, operations[index](17, 6));
    }
    return 0;
}
