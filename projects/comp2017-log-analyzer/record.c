/* Leon | Original teaching project. */
#include "record.h"

#include <stddef.h>
#include <string.h>

static bool is_space(char ch)
{
    return ch == ' ' || ch == '\t';
}

static const char *skip_space(const char *p)
{
    while (is_space(*p)) {
        ++p;
    }
    return p;
}

bool parse_record(const char *line, struct record *out)
{
    struct record candidate = {LEVEL_INFO, 0U};
    const char *start = skip_space(line);
    const char *p = start;

    while (*p != '\0' && !is_space(*p)) {
        ++p;
    }
    size_t length = (size_t)(p - start);
    if (length == 4 && memcmp(start, "INFO", 4) == 0) {
        candidate.level = LEVEL_INFO;
    } else if (length == 4 && memcmp(start, "WARN", 4) == 0) {
        candidate.level = LEVEL_WARN;
    } else if (length == 5 && memcmp(start, "ERROR", 5) == 0) {
        candidate.level = LEVEL_ERROR;
    } else {
        return false;
    }
    if (!is_space(*p)) {
        return false;
    }
    p = skip_space(p);
    if (*p < '0' || *p > '9') {
        return false;
    }
    while (*p >= '0' && *p <= '9') {
        unsigned digit = (unsigned)(*p - '0');
        if (candidate.duration_ms > (MAX_DURATION_MS - digit) / 10U) {
            return false;
        }
        candidate.duration_ms = candidate.duration_ms * 10U + digit;
        ++p;
    }
    if (*skip_space(p) != '\0') {
        return false;
    }
    *out = candidate;
    return true;
}
