// Guoliang | Original learning example
// Return success separately from the result
#include <stdio.h>
#include <stdlib.h>
static int parse_digit(const char *text, int *result) {
    if (text[0] < '0' || text[0] > '9')
        return 0;
    if (text[1] != '\0')
        return 0;
    *result = text[0] - '0';
    return 1;
}
int main(void) {
    const char *inputs[] = {"0", "7", "12", "", "x"};
    for (size_t i = 0; i < sizeof inputs / sizeof inputs[0]; i++) {
        int result = -1;
        int accepted = parse_digit(inputs[i], &result);
        printf("text='%s' accepted=%d result=%d\n", inputs[i], accepted, result);
    }
    return 0;
}
