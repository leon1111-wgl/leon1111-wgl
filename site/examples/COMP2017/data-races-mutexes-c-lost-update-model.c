// Leon | Original learning example
// Model a lost update without a C data race
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int shared = 10;
    int read_a = shared;
    int read_b = shared;
    shared = read_a - 1;
    printf("after A writes=%d\n", shared);
    shared = read_b - 1;
    printf("after B writes=%d\n", shared);
    printf("two completed decrements should give=%d\n", 10 - 2);
    puts("sequential model, not an executed data race");
    return 0;
}
