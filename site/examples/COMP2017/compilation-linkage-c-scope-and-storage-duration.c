// Guoliang | Original learning example
// Separate local scope from storage duration
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>

static void inspect(void) {
    int automatic = 0;
    static int persistent = 0;
    automatic++;
    persistent++;
    printf("automatic=%d persistent=%d\n", automatic, persistent);
}
int main(void) {
    inspect();
    inspect();
    inspect();
    return 0;
}
