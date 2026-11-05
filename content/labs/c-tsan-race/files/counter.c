/* counter: four worker threads handle fabricated requests and keep shared
 * totals, the way a small server counts traffic for its /metrics page. */
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>

#define WORKERS 4

struct stats {
    long requests;          /* how many requests were handled */
    long bytes;             /* total response bytes */
};

static struct stats stats;  /* shared by all workers */
static long per_worker = 50;

/* The size of request i handled by worker id: fixed, so runs are comparable. */
static long response_size(int id, long i)
{
    return 100 + (id * 7 + i) % 50;
}

static void *worker(void *arg)
{
    int id = (int)(long)arg;
    for (long i = 0; i < per_worker; i++) {
        long size = response_size(id, i);
        stats.requests++;
        stats.bytes += size;
    }
    return NULL;
}

int main(int argc, char **argv)
{
    if (argc > 1) {
        per_worker = atol(argv[1]);
    }

    pthread_t threads[WORKERS];
    for (int id = 0; id < WORKERS; id++) {
        pthread_create(&threads[id], NULL, worker, (void *)(long)id);
    }
    for (int id = 0; id < WORKERS; id++) {
        pthread_join(threads[id], NULL);
    }

    long want_requests = 0, want_bytes = 0;     /* single-threaded reference */
    for (int id = 0; id < WORKERS; id++) {
        for (long i = 0; i < per_worker; i++) {
            want_requests++;
            want_bytes += response_size(id, i);
        }
    }
    printf("requests=%ld (expected %ld)  bytes=%ld (expected %ld)\n",
           stats.requests, want_requests, stats.bytes, want_bytes);
    return (stats.requests == want_requests && stats.bytes == want_bytes) ? 0 : 1;
}
