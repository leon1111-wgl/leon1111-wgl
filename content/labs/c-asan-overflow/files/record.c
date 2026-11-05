/* record: a log record keeps its severity tag and numeric level together.
 * The tag is copied in by hand, one byte at a time, from the command line. */
#include <stdio.h>

struct record {
    char tag[8];        /* "INFO", "WARN", ... up to 7 characters + NUL */
    int level;          /* 1 = info, 2 = warn, 3 = error */
};

int main(int argc, char **argv)
{
    if (argc != 2) {
        fprintf(stderr, "usage: %s TAG\n", argv[0]);
        return 2;
    }
    struct record r = {"INFO", 1};
    int i = 0;
    do {
        r.tag[i] = argv[1][i];      /* no bound on i */
    } while (argv[1][i++] != '\0');
    printf("tag=%s level=%d\n", r.tag, r.level);
    return 0;
}
