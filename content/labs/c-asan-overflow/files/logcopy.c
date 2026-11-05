/* logcopy: read access-log lines and print an escaped copy of each one,
 * so a tab or a double quote inside a field cannot break the CSV loader
 * downstream. A tab becomes the two characters \t, a quote becomes \". */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define LINE_MAX_BYTES 256

/* Returns a heap copy of line with tabs and quotes escaped; caller frees. */
static char *escape_line(const char *line)
{
    size_t len = strlen(line);
    char *out = malloc(len + 1);              /* the text plus its NUL */
    if (out == NULL) {
        return NULL;
    }
    size_t j = 0;
    for (size_t i = 0; i < len; i++) {
        if (line[i] == '\t') {
            out[j++] = '\\';
            out[j++] = 't';
        } else if (line[i] == '"') {
            out[j++] = '\\';
            out[j++] = '"';
        } else {
            out[j++] = line[i];
        }
    }
    out[j] = '\0';
    return out;
}

int main(int argc, char **argv)
{
    if (argc != 2) {
        fprintf(stderr, "usage: %s file.log\n", argv[0]);
        return 2;
    }
    FILE *fp = fopen(argv[1], "r");
    if (fp == NULL) {
        perror(argv[1]);
        return 2;
    }
    char line[LINE_MAX_BYTES];
    int n = 0;
    while (fgets(line, sizeof line, fp) != NULL) {
        line[strcspn(line, "\n")] = '\0';      /* drop the newline */
        char *copy = escape_line(line);
        if (copy == NULL) {
            fclose(fp);
            return 1;
        }
        printf("%03d %s\n", ++n, copy);
        free(copy);
    }
    fclose(fp);
    return 0;
}
