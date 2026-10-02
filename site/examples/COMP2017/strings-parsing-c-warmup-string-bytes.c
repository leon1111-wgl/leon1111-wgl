// Guoliang | Original learning example
// Start here: a string needs an ending byte
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int main(void) {
    char message[6] = "Hi";
    size_t length = strlen(message);
    printf("capacity=%zu length=%zu\n", sizeof message, length);
    for (size_t i = 0; i < length; i++)
        printf("character %zu=%c\n", i, message[i]);
    printf("terminator is zero=%s\n", message[length] == '\0' ? "yes" : "no");
    message[1] = 'o';
    printf("after edit=%s\n", message);
    return 0;
}
