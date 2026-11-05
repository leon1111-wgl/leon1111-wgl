#include <stdio.h>
#include "ring.h"
#include "stats.h"
#include "util.h"

static int failures;

/* Counts a failed check and keeps going, so one run shows every failure. */
#define CHECK(cond) do { if (!(cond)) { \
    printf("FAIL %s:%d: %s\n", __FILE__, __LINE__, #cond); failures++; } } while (0)

int main(void)
{
    struct ring r;
    ring_init(&r);
    CHECK(ring_count(&r) == 0);

    for (int i = 1; i <= 20; i++) {
        ring_push(&r, i);                       /* 4 more than the window holds */
    }
    CHECK(ring_count(&r) == RING_CAPACITY);
    CHECK(ring_at(&r, 0) == 20);                /* newest */
    CHECK(ring_at(&r, 15) == 5);                /* oldest still in the window */
    CHECK(ring_at(&r, 16) == 0);                /* out of range */

    struct summary s = stats_summarise(&r);
    CHECK(s.min == 5 && s.max == 20);
    CHECK(s.mean > 12.49 && s.mean < 12.51);    /* (5 + ... + 20) / 16 */

    CHECK(hash_label("node-eu-west-1-0042") == 0x9baee89fu);

    if (failures != 0) {
        printf("test_ring: %d check(s) failed\n", failures);
        return 1;
    }
    puts("test_ring: all checks passed");
    return 0;
}
