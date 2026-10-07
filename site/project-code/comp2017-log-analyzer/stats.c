/* Leon | Original teaching project. */
#include "stats.h"
#include "reader.h"

#include <inttypes.h>

_Static_assert((uint64_t)MAX_INPUT_BYTES <= UINT64_MAX / MAX_DURATION_MS,
               "The byte budget must keep duration totals representable");

void stats_accept(struct stats *s, const struct record *record)
{
    if (s->valid == 0 || record->duration_ms < s->min_ms) {
        s->min_ms = record->duration_ms;
    }
    if (s->valid == 0 || record->duration_ms > s->max_ms) {
        s->max_ms = record->duration_ms;
    }
    ++s->lines;
    ++s->valid;
    ++s->by_level[record->level];
    s->total_ms += record->duration_ms;
}

void stats_reject(struct stats *s)
{
    ++s->lines;
    ++s->malformed;
}

bool stats_print(FILE *output, const struct stats *s)
{
    if (fprintf(output,
                "lines=%" PRIu64 "\nvalid=%" PRIu64 "\nmalformed=%" PRIu64 "\n"
                "INFO=%" PRIu64 "\nWARN=%" PRIu64 "\nERROR=%" PRIu64 "\n"
                "total_ms=%" PRIu64 "\n",
                s->lines, s->valid, s->malformed,
                s->by_level[LEVEL_INFO], s->by_level[LEVEL_WARN],
                s->by_level[LEVEL_ERROR], s->total_ms) < 0) {
        return false;
    }
    if (s->valid == 0) {
        if (fputs("min_ms=n/a\nmax_ms=n/a\nmean_ms=n/a\n", output) == EOF) {
            return false;
        }
    } else {
        double mean = (double)s->total_ms / (double)s->valid;
        if (fprintf(output, "min_ms=%u\nmax_ms=%u\nmean_ms=%.3f\n",
                    s->min_ms, s->max_ms, mean) < 0) {
            return false;
        }
    }
    return fflush(output) == 0;
}
