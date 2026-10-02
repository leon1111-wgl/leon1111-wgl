// Guoliang | Original learning example
// Test the last payload byte and its terminator
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static int copy_text(char *destination, size_t capacity, const char *source) {
    size_t length = strlen(source);
    if (length >= capacity)
        return 0;
    memcpy(destination, source, length + 1);
    return 1;
}
int main(void) {
    const char *inputs[] = {"", "1234567", "12345678", "12345678901"};
    for (size_t i = 0; i < sizeof inputs / sizeof inputs[0]; i++) {
        char destination[8] = "kept";
        int accepted = copy_text(destination, sizeof destination, inputs[i]);
        printf("length=%zu accepted=%d stored='%s'\n", strlen(inputs[i]), accepted,
               destination);
    }
    return 0;
}
