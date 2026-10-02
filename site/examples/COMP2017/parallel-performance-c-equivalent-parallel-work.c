// Guoliang | Original learning example
// Check equivalent work before benchmarking
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

struct Job {
    const int *values;
    size_t begin;
    size_t end;
    long result;
};
static void *sum_range(void *argument) {
    struct Job *job = argument;
    long total = 0;
    for (size_t i = job->begin; i < job->end; i++)
        total += job->values[i];
    job->result = total;
    return NULL;
}
int main(void) {
    enum { COUNT = 100, WORKERS = 4 };
    int values[COUNT];
    long serial = 0;
    for (size_t i = 0; i < COUNT; i++) {
        values[i] = (int)i + 1;
        serial += values[i];
    }
    struct Job jobs[WORKERS];
    pthread_t threads[WORKERS];
    for (size_t i = 0; i < WORKERS; i++) {
        jobs[i] =
            (struct Job){values, i * COUNT / WORKERS, (i + 1) * COUNT / WORKERS, 0};
        check_thread(pthread_create(&threads[i], NULL, sum_range, &jobs[i]));
    }
    long parallel = 0;
    for (size_t i = 0; i < WORKERS; i++) {
        check_thread(pthread_join(threads[i], NULL));
        parallel += jobs[i].result;
    }
    printf("serial=%ld parallel=%ld\n", serial, parallel);
    printf("same result=%s workers=%d\n", serial == parallel ? "yes" : "no", WORKERS);
    return serial == parallel ? 0 : 1;
}
