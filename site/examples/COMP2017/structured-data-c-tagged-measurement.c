// Guoliang | Original learning example
// Read a union through its tag
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>

enum Kind { COUNT, TEMPERATURE };
struct Measurement {
    enum Kind kind;
    union {
        int count;
        double temperature;
    } data;
};
static void show(const struct Measurement *value) {
    switch (value->kind) {
    case COUNT:
        printf("count=%d\n", value->data.count);
        break;
    case TEMPERATURE:
        printf("temperature=%.1f\n", value->data.temperature);
        break;
    }
}
int main(void) {
    struct Measurement value = {COUNT, {.count = 7}};
    show(&value);
    value.data.temperature = 18.5;
    value.kind = TEMPERATURE;
    show(&value);
    return 0;
}
