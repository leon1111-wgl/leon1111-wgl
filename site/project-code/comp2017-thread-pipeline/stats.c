/* Leon | Original teaching project. */
#include "stats.h"

#include <errno.h>
#include <fcntl.h>
#include <stdbool.h>
#include <sys/stat.h>
#include <unistd.h>

/* Fixed ASCII separators make results independent of process locale. */
static bool separator(unsigned char byte) {
    return byte == ' ' || byte == '\t' || byte == '\n' || byte == '\r' ||
           byte == '\v' || byte == '\f';
}

static void count_stream(int descriptor, FileStats *result) {
    unsigned char buffer[4096];
    bool in_word = false;
    unsigned char last = '\n';
    for (;;) {
        ssize_t received = read(descriptor, buffer, sizeof buffer);
        if (received < 0) {
            if (errno == EINTR) {
                continue;
            }
            result->status = SCAN_READ;
            result->system_error = errno;
            return;
        }
        if (received == 0) {
            break;
        }
        size_t length = (size_t)received;
        if (length > FILE_BYTE_LIMIT - result->bytes) {
            result->status = SCAN_TOO_LARGE;
            return;
        }
        result->bytes += length;
        for (size_t i = 0; i < length; i++) {
            unsigned char byte = buffer[i];
            if (byte == '\n') {
                result->lines++;
            }
            bool space = separator(byte);
            if (!space && !in_word) {
                result->words++;
            }
            in_word = !space;
            last = byte;
        }
    }
    if (result->bytes != 0 && last != '\n') {
        result->lines++;
    }
}

void scan_file(const char *path, FileStats *result) {
    *result = (FileStats){0};
    /* Nonblocking open avoids waiting forever for a FIFO writer. Only a
       regular file is accepted after opening; each worker owns its fd. */
    int descriptor = open(path, O_RDONLY | O_NONBLOCK);
    if (descriptor < 0) {
        result->status = SCAN_OPEN;
        result->system_error = errno;
        return;
    }
    struct stat info;
    if (fstat(descriptor, &info) != 0) {
        result->status = SCAN_METADATA;
        result->system_error = errno;
    } else if (!S_ISREG(info.st_mode)) {
        result->status = SCAN_NOT_REGULAR;
    } else {
        count_stream(descriptor, result);
    }
    /* Preserve the first error; do not retry close after an uncertain result. */
    if (close(descriptor) != 0 && result->status == SCAN_OK) {
        result->status = SCAN_CLOSE;
        result->system_error = errno;
    }
}

const char *scan_status_name(ScanStatus status) {
    switch (status) {
        case SCAN_OK: return "ok";
        case SCAN_OPEN: return "open";
        case SCAN_METADATA: return "metadata";
        case SCAN_NOT_REGULAR: return "not-regular";
        case SCAN_READ: return "read";
        case SCAN_TOO_LARGE: return "too-large";
        case SCAN_CLOSE: return "close";
    }
    return "unknown";
}
