#include "ring.h"

void ring_init(struct ring *r)
{
    r->head = 0;
    r->count = 0;
}

void ring_push(struct ring *r, int sample)
{
    r->data[r->head] = sample;
    r->head = (r->head + 1) % RING_CAPACITY;
    if (r->count < RING_CAPACITY) {
        r->count++;
    }
}

size_t ring_count(const struct ring *r)
{
    return r->count;
}

int ring_at(const struct ring *r, size_t age)
{
    if (age >= r->count) {
        return 0;
    }
    return r->data[(r->head + RING_CAPACITY - 1 - age) % RING_CAPACITY];
}
