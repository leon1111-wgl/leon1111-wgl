// Guoliang | Original learning example
// Start here: pass one operation into a loop
#include <stdio.h>
#include <stdlib.h>
typedef int (*Transform)(int);
static int double_small(int value) {
    return value * 2;
}
static int add_one_small(int value) {
    return value + 1;
}
static void print_transformed(const int *values, size_t count, Transform action) {
    for (size_t i = 0; i < count; i++)
        printf("%s%d", i == 0 ? "" : " ", action(values[i]));
    putchar('\n');
}
int main(void) {
    const int values[] = {1, 2, 3};
    print_transformed(values, 3, double_small);
    print_transformed(values, 3, add_one_small);
    printf("original=%d,%d,%d\n", values[0], values[1], values[2]);
    return 0;
}
