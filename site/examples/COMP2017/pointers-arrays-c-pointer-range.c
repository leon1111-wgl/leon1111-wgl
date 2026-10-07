// Leon | Original learning example
// Traverse with a begin and end pointer
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int values[] = {3, 5, 8};
    size_t count = sizeof values / sizeof values[0];
    const int *begin = values;
    const int *end = values + count;
    int total = 0;
    for (const int *cursor = begin; cursor != end; cursor++) {
        total += *cursor;
    }
    printf("elements=%td\n", end - begin);
    printf("sum=%d\n", total);
    return 0;
}
