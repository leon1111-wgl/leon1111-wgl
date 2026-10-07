/* Leon | Original teaching project. */
#include "process.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>

static int parse_capacity(const char *text, size_t *capacity)
{
    size_t value = 0;
    if (*text == '\0') {
        return -1;
    }
    for (const char *p = text; *p != '\0'; ++p) {
        if (*p < '0' || *p > '9') {
            return -1;
        }
        size_t digit = (size_t)(*p - '0');
        if (value > (PROCESS_MAX_CAPTURE - digit) / 10) {
            return -1;
        }
        value = value * 10 + digit;
    }
    *capacity = value;
    return 0;
}

/* A byte view: no strlen on captured data, and no raw terminal controls. */
static void print_bytes(const unsigned char *data, size_t length)
{
    fputs("stdout=\"", stdout);
    for (size_t i = 0; i < length; ++i) {
        unsigned char byte = data[i];
        switch (byte) {
        case '\n': fputs("\\n", stdout); break;
        case '\r': fputs("\\r", stdout); break;
        case '\t': fputs("\\t", stdout); break;
        case '\\': fputs("\\\\", stdout); break;
        case '"': fputs("\\\"", stdout); break;
        default:
            if (byte >= 32 && byte <= 126) {
                putchar((int)byte);
            } else {
                printf("\\x%02X", (unsigned int)byte);
            }
        }
    }
    puts("\"");
}

static int report(const unsigned char *data, const struct process_result *result)
{
    print_bytes(data, result->captured);
    printf("captured_bytes=%zu\ntruncated=%s\n", result->captured,
           result->truncated ? "yes" : "no");
    if (WIFEXITED(result->wait_status)) {
        int code = WEXITSTATUS(result->wait_status);
        printf("child_exit=%d\n", code);
        return code;
    }
    if (WIFSIGNALED(result->wait_status)) {
        int number = WTERMSIG(result->wait_status);
        printf("child_signal=%d\n", number);
        return 128 + number;
    }
    fputs("process_runner: unexpected wait status\n", stderr);
    return 125;
}

int main(int argc, char **argv)
{
    size_t capacity;
    if (argc < 4 || strcmp(argv[2], "--") != 0 || argv[3][0] == '\0' ||
        parse_capacity(argv[1], &capacity) == -1) {
        fputs("usage: process_runner CAP -- PROGRAM [ARG ...]\n"
              "CAP must be decimal digits from 0 to 65536.\n", stderr);
        return 2;
    }
    unsigned char *data = malloc(capacity > 0 ? capacity : 1);
    if (data == NULL) {
        fputs("process_runner: allocation failed\n", stderr);
        return 125;
    }
    struct process_result result;
    if (process_run(&argv[3], data, capacity, &result) == -1) {
        perror("process_runner");
        free(data);
        return 125;
    }
    int code = report(data, &result);
    free(data);
    if (fflush(stdout) == EOF || ferror(stdout)) {
        fputs("process_runner: report write failed\n", stderr);
        return 125;
    }
    return code;
}
