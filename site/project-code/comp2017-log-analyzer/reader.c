/* Leon | Original teaching project. */
#include "reader.h"

#include <stdbool.h>

enum line_status read_line(struct line_reader *reader,
                           char line[MAX_LINE_BYTES + 1U])
{
    size_t used = 0;
    bool seen_byte = false;
    bool bad = false;

    for (;;) {
        int ch = fgetc(reader->stream);
        if (ch == EOF) {
            if (ferror(reader->stream)) {
                return LINE_IO_ERROR;
            }
            if (!seen_byte) {
                return LINE_END;
            }
            break;
        }
        if (reader->bytes_read == MAX_INPUT_BYTES) {
            return LINE_LIMIT;
        }
        ++reader->bytes_read;
        seen_byte = true;
        if (ch == '\n') {
            break;
        }
        if (ch == '\0' || used == MAX_LINE_BYTES) {
            bad = true;
        }
        if (!bad) {
            line[used++] = (char)ch;
        }
        /* Keep consuming a bad line so its tail is not a new record. */
    }
    if (bad) {
        return LINE_BAD;
    }
    if (used > 0 && line[used - 1] == '\r') {
        --used;
    }
    line[used] = '\0';
    return LINE_OK;
}
