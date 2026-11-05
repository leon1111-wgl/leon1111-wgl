#ifndef RING_H
#define RING_H

#include <stddef.h>

#define RING_CAPACITY 16

/* A window over the most recent RING_CAPACITY integer samples. */
struct ring {
    int data[RING_CAPACITY];
    size_t head;                /* index where the next sample is written */
    size_t count;               /* valid samples, at most RING_CAPACITY */
};

void ring_init(struct ring *r);

/* Adds a sample; once the window is full the oldest sample is overwritten. */
void ring_push(struct ring *r, int sample);

size_t ring_count(const struct ring *r);

/* Sample number `age` counted from the newest (0 = newest); 0 if out of range. */
int ring_at(const struct ring *r, size_t age);

#endif
