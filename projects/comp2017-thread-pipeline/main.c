/* Leon | Original teaching project. */
#include "queue.h"
#include "stats.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_WORKERS 16u
#define MAX_JOBS 128u

typedef struct {
    WorkQueue *queue;
    char **paths;
    FileStats *results;
} WorkerContext;

static bool parse_workers(const char *text, size_t *workers) {
    size_t value = 0;
    if (*text == '\0') {
        return false;
    }
    for (const unsigned char *p = (const unsigned char *)text; *p != '\0'; p++) {
        if (*p < '0' || *p > '9') {
            return false;
        }
        value = value * 10 + (size_t)(*p - '0');
        if (value > MAX_WORKERS) {
            return false;
        }
    }
    if (value == 0) {
        return false;
    }
    *workers = value;
    return true;
}

static void *consume(void *argument) {
    WorkerContext *context = argument;
    size_t job;
    while (queue_pop(context->queue, &job)) {
        /* Exactly one pop receives each index. No other worker writes this
           result, and main waits for all joins before reading any result. */
        scan_file(context->paths[job], &context->results[job]);
    }
    return NULL;
}

static void join_workers(pthread_t *threads, size_t count) {
    for (size_t i = 0; i < count; i++) {
        thread_check(pthread_join(threads[i], NULL), "thread join");
    }
}

static int print_results(char **paths, FileStats *results, size_t count) {
    size_t failures = 0;
    for (size_t i = 0; i < count; i++) {
        FileStats *result = &results[i];
        if (result->status == SCAN_OK) {
            printf("job=%zu bytes=%zu lines=%zu words=%zu\n",
                   i + 1, result->bytes, result->lines, result->words);
        } else {
            const char *kind = scan_status_name(result->status);
            printf("job=%zu error=%s\n", i + 1, kind);
            fprintf(stderr, "job %zu (%s): %s", i + 1, paths[i], kind);
            if (result->system_error != 0) {
                fprintf(stderr, ": %s", strerror(result->system_error));
            }
            fputc('\n', stderr);
            failures++;
        }
    }
    printf("summary files=%zu ok=%zu failed=%zu\n",
           count, count - failures, failures);
    if (fflush(stdout) != 0 || ferror(stdout)) {
        fputs("output failed\n", stderr);
        return EXIT_FAILURE;
    }
    return failures == 0 ? EXIT_SUCCESS : EXIT_FAILURE;
}

int main(int argc, char **argv) {
    size_t workers;
    if (argc < 2 || !parse_workers(argv[1], &workers) ||
        (size_t)(argc - 2) > MAX_JOBS) {
        fputs("usage: thread_pipeline WORKERS [FILE ...]\n"
              "WORKERS: 1..16; FILE: 0..128 regular files, each <= 8388608 bytes\n",
              stderr);
        return 2;
    }
    size_t jobs = (size_t)(argc - 2);
    WorkQueue queue;
    int error = queue_init(&queue);
    if (error != 0) {
        fprintf(stderr, "queue initialization failed (pthread error %d)\n", error);
        return EXIT_FAILURE;
    }
    FileStats results[MAX_JOBS] = {{0}};
    pthread_t threads[MAX_WORKERS];
    WorkerContext context = {&queue, argv + 2, results};
    size_t started = 0;
    for (; started < workers; started++) {
        error = pthread_create(&threads[started], NULL, consume, &context);
        if (error != 0) {
            fprintf(stderr, "thread creation failed after %zu workers "
                            "(pthread error %d)\n", started, error);
            /* No jobs are published until the whole pool exists. */
            queue_close(&queue);
            join_workers(threads, started);
            queue_destroy(&queue);
            return EXIT_FAILURE;
        }
    }
    for (size_t job = 0; job < jobs; job++) {
        if (!queue_push(&queue, job)) {
            fputs("internal error: queue closed during production\n", stderr);
            queue_close(&queue);
            join_workers(threads, started);
            queue_destroy(&queue);
            return EXIT_FAILURE;
        }
    }
    queue_close(&queue);
    join_workers(threads, started);
    queue_destroy(&queue);
    return print_results(argv + 2, results, jobs);
}
