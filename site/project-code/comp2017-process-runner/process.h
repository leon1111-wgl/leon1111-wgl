/* Leon | Original teaching project. */
#ifndef LEON_PROCESS_H
#define LEON_PROCESS_H

#include <stdbool.h>
#include <stddef.h>

#define PROCESS_MAX_CAPTURE 65536U

struct process_result {
    size_t captured;
    bool truncated;
    int wait_status;
};

/* Synchronous, single-threaded caller; standard descriptors 0, 1, 2 must be open.
 * argv is a nonempty, NULL-terminated argument vector, borrowed for this call.
 * buffer belongs to the caller and holds at least capacity bytes (0 is valid).
 * Return 0 after reaping the direct child, even if it failed. On -1, errno
 * describes a runner error; do not consume result. No timeout is provided. */
int process_run(char *const argv[], unsigned char *buffer, size_t capacity,
                struct process_result *result);

#endif
