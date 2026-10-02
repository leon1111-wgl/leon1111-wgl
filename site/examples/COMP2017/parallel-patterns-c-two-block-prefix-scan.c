// Guoliang | Original learning example
// Join local prefixes before applying offsets
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <string.h>
static void check_thread(int code) {
    if (code != 0) {
        fprintf(stderr, "pthread error: %s\n", strerror(code));
        exit(EXIT_FAILURE);
    }
}

struct Block {
    const int *input;
    int *output;
    size_t count;
    int total;
};
static void *local_prefix(void *argument) {
    struct Block *job = argument;
    int total = 0;
    for (size_t i = 0; i < job->count; i++) {
        total += job->input[i];
        job->output[i] = total;
    }
    job->total = total;
    return NULL;
}
int main(void) {
    const int input[] = {2, 1, 3, 4, 2, 5};
    int output[6] = {0};
    struct Block blocks[2] = {{input, output, 3, 0}, {input + 3, output + 3, 3, 0}};
    pthread_t threads[2];
    for (size_t i = 0; i < 2; i++)
        check_thread(pthread_create(&threads[i], NULL, local_prefix, &blocks[i]));
    for (size_t i = 0; i < 2; i++)
        check_thread(pthread_join(threads[i], NULL));
    printf("block totals=%d %d\n", blocks[0].total, blocks[1].total);
    int offset = 0;
    for (size_t b = 0; b < 2; b++) {
        for (size_t i = 0; i < blocks[b].count; i++)
            blocks[b].output[i] += offset;
        offset += blocks[b].total;
    }
    for (size_t i = 0; i < 6; i++)
        printf("%s%d", i ? " " : "", output[i]);
    putchar('\n');
    return 0;
}
