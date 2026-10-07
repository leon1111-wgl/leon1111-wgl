/* Leon | Original teaching project. */
#ifndef RECORD_H
#define RECORD_H

#include <stdbool.h>

#define MAX_DURATION_MS 60000U

enum log_level { LEVEL_INFO, LEVEL_WARN, LEVEL_ERROR, LEVEL_COUNT };

struct record {
    enum log_level level;
    unsigned duration_ms;
};

/* line: readable NUL-terminated text; out: writable caller-owned record.
 * Return true and assign *out only for a complete valid record.
 * Neither pointer is retained; a failed parse leaves *out unchanged. */
bool parse_record(const char *line, struct record *out);

#endif
