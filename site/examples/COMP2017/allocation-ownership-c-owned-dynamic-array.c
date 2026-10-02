// Guoliang | Original learning example
// Allocate, initialize, use and release
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(void) {
    size_t n = 6;
    int *values = NULL;
    if (n > SIZE_MAX / sizeof *values)
        return 1;
    values = malloc(n * sizeof *values);
    if (values == NULL)
        return 1;
    int total = 0;
    for (size_t i = 0; i < n; i++) {
        values[i] = (int)i + 1;
        total += values[i];
    }
    printf("count=%zu sum=%d\n", n, total);
    free(values);
    values = NULL;
    puts("owner cleared");
    return 0;
}
