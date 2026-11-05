#include "stats.h"

struct summary stats_summarise(const struct ring *r)
{
    struct summary s = {0, 0, 0.0};
    size_t n = ring_count(r);
    if (n == 0) {
        return s;
    }
    long sum = 0;
    s.min = s.max = ring_at(r, 0);
    for (int i = 0; i < n; i++) {
        int v = ring_at(r, (size_t)i);
        if (v < s.min) {
            s.min = v;
        }
        if (v > s.max) {
            s.max = v;
        }
        sum += v;
    }
    s.mean = (double)sum / (double)n;
    return s;
}
