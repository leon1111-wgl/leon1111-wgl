// Leon | Original learning example
// Start here: one allocation, one owner, one release
#include <stdio.h>
#include <stdlib.h>
static void release_values(int **owner) {
    free(*owner);
    *owner = NULL;
}
int main(void) {
    size_t count = 3;
    int *values = malloc(count * sizeof *values);
    if (values == NULL) {
        fputs("allocation failed\n", stderr);
        return 1;
    }
    for (size_t i = 0; i < count; i++)
        values[i] = (int)(i + 1) * 10;
    printf("values=%d,%d,%d\n", values[0], values[1], values[2]);
    release_values(&values);
    printf("owner cleared=%s\n", values == NULL ? "yes" : "no");
    release_values(&values);
    puts("releasing a null owner is allowed");
    return 0;
}
