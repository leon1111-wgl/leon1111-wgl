/* Leon | Original teaching project. */
#include <signal.h>
#include <stdio.h>
#include <string.h>

/* Synthetic, finite output only: no files, descendants, input, or sleeps. */
int main(int argc, char **argv)
{
    if (argc < 2) {
        return 2;
    }
    if (strcmp(argv[1], "args") == 0) {
        for (int i = 2; i < argc; ++i) {
            printf("[%s]", argv[i]);
        }
    } else if (strcmp(argv[1], "burst") == 0) {
        char block[4096];
        memset(block, 'A', sizeof(block));
        for (int i = 0; i < 256; ++i) {
            if (fwrite(block, 1, sizeof(block), stdout) != sizeof(block)) {
                return 3;
            }
        }
    } else if (strcmp(argv[1], "fragment") == 0) {
        fputs("tail", stdout);
    } else if (strcmp(argv[1], "fail") == 0) {
        puts("check failed");
        return 7;
    } else if (strcmp(argv[1], "stderr") == 0) {
        fputs("diagnostic\n", stderr);
        puts("ok");
    } else if (strcmp(argv[1], "bytes") == 0) {
        const unsigned char bytes[] = {0, 255, '"', '\\', '\t', '\r', '\n'};
        if (fwrite(bytes, 1, sizeof(bytes), stdout) != sizeof(bytes)) {
            return 3;
        }
    } else if (strcmp(argv[1], "signal") == 0) {
        (void)raise(SIGTERM);
        return 3;
    } else if (strcmp(argv[1], "empty") != 0) {
        return 2;
    }
    return fflush(stdout) == 0 ? 0 : 3;
}
