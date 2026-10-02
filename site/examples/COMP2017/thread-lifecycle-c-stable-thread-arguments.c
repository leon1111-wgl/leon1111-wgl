// Guoliang | Original learning example
// Keep one argument record per worker
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
    int begin;
    int end;
    int sum;
};
static void *worker(void *argument) {
    struct Job *job = argument;
    int total = 0;
    for (int i = job->begin; i < job->end; i++)
        total += i;
    job->sum = total;
    return NULL;
}
int main(void) {
    struct Job jobs[2] = {{0, 5, 0}, {5, 10, 0}};
    pthread_t threads[2];
    size_t created = 0;
    for (; created < 2; created++) {
        int error = pthread_create(&threads[created], NULL, worker, &jobs[created]);
        if (error != 0)
            break;
    }
    for (size_t i = 0; i < created; i++)
        check_thread(pthread_join(threads[i], NULL));
    if (created != 2)
        return 1;
    printf("first=%d second=%d total=%d\n", jobs[0].sum, jobs[1].sum,
           jobs[0].sum + jobs[1].sum);
    return 0;
}
