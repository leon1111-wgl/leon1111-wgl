// Leon | Original learning example
// Commit a resize only after success
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(void) {
    size_t old_count = 3, new_count = 5;
    int *values = malloc(old_count * sizeof *values);
    if (values == NULL)
        return 1;
    for (size_t i = 0; i < old_count; i++)
        values[i] = (int)i + 1;
    if (new_count > SIZE_MAX / sizeof *values) {
        free(values);
        return 1;
    }
    int *resized = realloc(values, new_count * sizeof *values);
    if (resized == NULL) {
        free(values);
        return 1;
    }
    values = resized;
    for (size_t i = old_count; i < new_count; i++)
        values[i] = (int)i + 1;
    for (size_t i = 0; i < new_count; i++)
        printf("%s%d", i ? " " : "", values[i]);
    putchar('\n');
    free(values);
    return 0;
}
