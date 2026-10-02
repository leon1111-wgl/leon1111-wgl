// Guoliang | Original learning example
// Use an interface before its definition
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>

int add(int, int);
extern int total;
static int helper(int left, int right) {
    return left + right;
}
int add(int left, int right) {
    return helper(left, right);
}
int total = 0;
int main(void) {
    total = add(8, 5);
    printf("total=%d\n", total);
    return 0;
}
