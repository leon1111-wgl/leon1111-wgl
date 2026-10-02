// Guoliang | Original learning example
// Distinguish presence from numeric truth
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>

#define ENABLE_CACHE 0
int main(void) {
#ifdef ENABLE_CACHE
    puts("macro exists");
#else
    puts("macro absent");
#endif
#if ENABLE_CACHE
    puts("cache enabled");
#else
    puts("cache disabled");
#endif
    printf("active function=%s\n", __func__);
    return 0;
}
