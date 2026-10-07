// Leon | Original learning example
// Separate text length from storage capacity
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
    char text[] = "lamp";
    text[0] = 'L';
    printf("text=%s length=%zu capacity=%zu\n", text, strlen(text), sizeof text);
    char small[4];
    int needed = snprintf(small, sizeof small, "%s", "Maple");
    if (needed < 0)
        return 1;
    printf("stored=%s required=%d\n", small, needed);
    printf("truncated=%s\n", (size_t)needed >= sizeof small ? "yes" : "no");
    return 0;
}
