#ifndef STATS_H
#define STATS_H

#include "ring.h"

struct summary {
    int min;
    int max;
    double mean;
};

/* Summarises the samples in the window. An empty window gives all zeros. */
struct summary stats_summarise(const struct ring *r);

#endif
