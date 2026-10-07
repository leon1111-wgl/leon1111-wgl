/* Leon | Original teaching project. */
#ifndef STATS_H
#define STATS_H

#include <stddef.h>

#define FILE_BYTE_LIMIT (8u * 1024u * 1024u)

typedef enum {
    SCAN_OK,
    SCAN_OPEN,
    SCAN_METADATA,
    SCAN_NOT_REGULAR,
    SCAN_READ,
    SCAN_TOO_LARGE,
    SCAN_CLOSE
} ScanStatus;

typedef struct {
    size_t bytes;
    size_t lines;
    size_t words;
    ScanStatus status;
    int system_error;
} FileStats;

/* The caller exclusively owns *result until this call returns.
   Failure counters are partial and must not be reported as valid counts. */
void scan_file(const char *path, FileStats *result);
const char *scan_status_name(ScanStatus status);

#endif
