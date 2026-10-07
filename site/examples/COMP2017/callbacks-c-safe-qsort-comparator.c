// Leon | Original learning example
// Sort without subtracting arbitrary integers
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
static int compare_int(const void *left, const void *right) {
    int a = *(const int *)left;
    int b = *(const int *)right;
    return (a > b) - (a < b);
}
int main(void) {
    int minimum = INT_MIN, maximum = INT_MAX;
    printf("extreme comparison=%d\n", compare_int(&minimum, &maximum));
    int values[] = {4, -7, 0, -7};
    size_t count = sizeof values / sizeof values[0];
    qsort(values, count, sizeof values[0], compare_int);
    for (size_t i = 0; i < count; i++)
        printf("%s%d", i ? " " : "", values[i]);
    putchar('\n');
    return 0;
}
