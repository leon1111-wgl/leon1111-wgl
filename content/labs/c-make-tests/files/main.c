#include <stdio.h>
#include "ring.h"
#include "stats.h"
#include "util.h"

int main(int argc, char **argv)
{
    struct ring r;
    ring_init(&r);

    unsigned seed = 12345u;                     /* fixed seed: same samples every run */
    for (int i = 0; i < 20; i++) {
        seed = seed * 1103515245u + 12345u;
        ring_push(&r, (int)((seed >> 16) % 200));
    }

    struct summary s = stats_summarise(&r);
    printf("%zu samples, min %d, max %d, mean %.2f\n", ring_count(&r), s.min, s.max, s.mean);
    printf("shard key %08x\n", hash_label("node-eu-west-1-0042"));
    return 0;
}
