// Guoliang | Original learning example
// Give each matrix row one writer
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

static const int left[2][2] = {{1, 2}, {3, 4}};
static const int right[2][2] = {{2, 0}, {1, 5}};
static int result[2][2];
struct Row {
    size_t index;
};
static void *multiply_row(void *argument) {
    const struct Row *job = argument;
    size_t r = job->index;
    for (size_t c = 0; c < 2; c++) {
        int total = 0;
        for (size_t k = 0; k < 2; k++)
            total += left[r][k] * right[k][c];
        result[r][c] = total;
    }
    return NULL;
}
int main(void) {
    struct Row jobs[2] = {{0}, {1}};
    pthread_t threads[2];
    for (size_t i = 0; i < 2; i++)
        check_thread(pthread_create(&threads[i], NULL, multiply_row, &jobs[i]));
    for (size_t i = 0; i < 2; i++)
        check_thread(pthread_join(threads[i], NULL));
    for (size_t r = 0; r < 2; r++)
        printf("row %zu: %d %d\n", r, result[r][0], result[r][1]);
    return 0;
}
