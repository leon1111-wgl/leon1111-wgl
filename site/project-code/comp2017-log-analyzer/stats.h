/* Leon | Original teaching project. */
#ifndef STATS_H
#define STATS_H

#include "record.h"

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

struct stats {
    uint64_t lines;
    uint64_t valid;
    uint64_t malformed;
    uint64_t by_level[LEVEL_COUNT];
    uint64_t total_ms;
    unsigned min_ms;
    unsigned max_ms;
};

/* Start with struct stats s = {0}. Add at most MAX_INPUT_BYTES records.
 * record must come from a successful parse_record call.
 * All pointers are borrowed for the duration of each call. */
void stats_accept(struct stats *s, const struct record *record);
void stats_reject(struct stats *s);

/* Write the final summary; false means a write/flush error.
 * A failed output may already contain a prefix. Do not close output here. */
bool stats_print(FILE *output, const struct stats *s);

#endif
