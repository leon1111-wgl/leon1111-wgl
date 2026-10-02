// Guoliang | Original learning example
// Calculate an ideal bound and explicit overhead
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    double serial_fraction = 0.2;
    int processors[] = {1, 2, 4, 8};
    for (size_t i = 0; i < sizeof processors / sizeof processors[0]; i++) {
        int p = processors[i];
        double speedup = 1.0 / (serial_fraction + (1.0 - serial_fraction) / p);
        printf("p=%d ideal speedup=%.3f efficiency=%.3f\n", p, speedup, speedup / p);
    }
    double serial_seconds = 10.0;
    double ideal_seconds =
        serial_seconds * (serial_fraction + (1.0 - serial_fraction) / 4.0);
    double with_overhead = ideal_seconds + 0.5;
    printf("four-worker model seconds=%.1f with overhead=%.1f\n", ideal_seconds,
           with_overhead);
    printf("overhead model speedup=%.3f limit=%.1f\n", serial_seconds / with_overhead,
           1.0 / serial_fraction);
    return 0;
}
