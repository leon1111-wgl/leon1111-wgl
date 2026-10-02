// Guoliang | Original learning example
// Copy embedded data and share pointed-to data
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>

struct Record {
    char label[4];
    int *borrowed;
};
int main(void) {
    int shared[] = {4, 7};
    struct Record original = {{'o', 'a', 'k', '\0'}, shared};
    struct Record copy = original;
    copy.label[0] = 'O';
    copy.borrowed[0] = 9;
    printf("original label=%s value=%d\n", original.label, original.borrowed[0]);
    printf("copy label=%s value=%d\n", copy.label, copy.borrowed[0]);
    return 0;
}
