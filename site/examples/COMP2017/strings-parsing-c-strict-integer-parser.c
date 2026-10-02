// Guoliang | Original learning example
// Validate the entire integer input
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <limits.h>
#include <ctype.h>
static int parse_int(const char *text, int *output) {
    char *end;
    errno = 0;
    long value = strtol(text, &end, 10);
    if (end == text || errno == ERANGE || value < INT_MIN || value > INT_MAX)
        return 0;
    while (isspace((unsigned char)*end))
        end++;
    if (*end != '\0')
        return 0;
    *output = (int)value;
    return 1;
}
int main(void) {
    const char *inputs[] = {"42x", " 42 ", "", "99999999999999999999999999999999"};
    for (size_t i = 0; i < sizeof inputs / sizeof inputs[0]; i++) {
        int value = 0;
        if (parse_int(inputs[i], &value))
            printf("input %zu accepted=%d\n", i, value);
        else
            printf("input %zu rejected\n", i);
    }
    return 0;
}
