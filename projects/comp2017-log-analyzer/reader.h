/* Leon | Original teaching project. */
#ifndef READER_H
#define READER_H

#include <stddef.h>
#include <stdio.h>

#define MAX_LINE_BYTES 127U
#define MAX_INPUT_BYTES 1048576U

enum line_status { LINE_OK, LINE_BAD, LINE_END, LINE_IO_ERROR, LINE_LIMIT };

struct line_reader {
    FILE *stream;       /* Borrowed: only the caller closes this stream. */
    size_t bytes_read;  /* Start at zero; includes newline and CR bytes. */
};

/* Caller supplies MAX_LINE_BYTES + 1 writable bytes.
 * LINE_OK: complete NUL-terminated line, without LF or a final CR.
 * LINE_BAD: oversized or NUL-containing line was consumed through LF/EOF.
 * LINE_END: clean EOF with no pending line. Other results are fatal.
 * LINE_LIMIT may consume one byte beyond the budget to distinguish EOF.
 * Do not parse the buffer unless the result is LINE_OK. */
enum line_status read_line(struct line_reader *reader,
                           char line[MAX_LINE_BYTES + 1U]);

#endif
