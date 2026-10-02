/* Guoliang | Original teaching project. */
#include "reader.h"
#include "record.h"
#include "stats.h"

#include <inttypes.h>
#include <stdio.h>
#include <string.h>

enum exit_status { EXIT_CLEAN = 0, EXIT_IO = 1, EXIT_USAGE = 2, EXIT_DATA = 3 };
#define WARNING_LIMIT 5U

static void warn_bad_line(const struct stats *s)
{
    if (s->malformed <= WARNING_LIMIT) {
        fprintf(stderr, "warning: line %" PRIu64 ": malformed record\n", s->lines);
    } else if (s->malformed == WARNING_LIMIT + 1U) {
        fputs("warning: further malformed lines omitted\n", stderr);
    }
}

/* Borrow input and caller-owned statistics. Report only complete input. */
static bool analyze(FILE *input, struct stats *s)
{
    struct line_reader reader = {input, 0};
    char line[MAX_LINE_BYTES + 1U];

    for (;;) {
        enum line_status status = read_line(&reader, line);
        if (status == LINE_END) {
            return true;
        }
        if (status == LINE_IO_ERROR) {
            fputs("error: cannot read input\n", stderr);
            return false;
        }
        if (status == LINE_LIMIT) {
            fprintf(stderr, "error: input exceeds %u bytes\n", MAX_INPUT_BYTES);
            return false;
        }
        struct record record;
        if (status == LINE_BAD || !parse_record(line, &record)) {
            stats_reject(s);
            warn_bad_line(s);
        } else {
            stats_accept(s, &record);
        }
    }
}

int main(int argc, char **argv)
{
    if (argc != 2) {
        fputs("usage: log_analyzer FILE|-\n", stderr);
        return EXIT_USAGE;
    }
    bool owns_input = strcmp(argv[1], "-") != 0;
    FILE *input = owns_input ? fopen(argv[1], "rb") : stdin;
    if (input == NULL) {
        fprintf(stderr, "error: cannot open input: %s\n", argv[1]);
        return EXIT_IO;
    }

    struct stats totals = {0};
    bool completed = analyze(input, &totals);
    if (owns_input && fclose(input) != 0) {
        fputs("error: cannot close input\n", stderr);
        completed = false;
    }
    if (!completed) {
        return EXIT_IO;
    }
    if (!stats_print(stdout, &totals)) {
        fputs("error: cannot write report\n", stderr);
        return EXIT_IO;
    }
    return totals.malformed == 0 ? EXIT_CLEAN : EXIT_DATA;
}
