// Leon | Original learning example
// Compare token substitution with a function call
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>

#define BAD(x) x *x
#define SQUARE(x) ((x) * (x))
static inline int square(int x) {
    return x * x;
}
int main(void) {
    int a = 4;
    printf("ungrouped=%d\n", BAD(a + 1));
    printf("grouped=%d\n", SQUARE(a + 1));
    int i = 4;
    int result = square(i++);
    printf("function=%d next i=%d\n", result, i);
    return 0;
}
