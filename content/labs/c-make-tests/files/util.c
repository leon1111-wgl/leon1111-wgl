#include "util.h"

unsigned hash_label(const char *s)
{
    int h = 7;
    while (*s != '\0') {
        h = h * 31 + (unsigned char)*s++;
    }
    return (unsigned)h;
}
