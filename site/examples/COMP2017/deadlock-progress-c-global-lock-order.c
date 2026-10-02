// Guoliang | Original learning example
// Use one lock order for both directions
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

struct Resource {
    int rank;
    int units;
    pthread_mutex_t lock;
};
struct Move {
    struct Resource *from;
    struct Resource *to;
};
static void *move_units(void *argument) {
    struct Move *job = argument;
    struct Resource *first = job->from->rank < job->to->rank ? job->from : job->to;
    struct Resource *second = first == job->from ? job->to : job->from;
    for (int i = 0; i < 50; i++) {
        check_thread(pthread_mutex_lock(&first->lock));
        check_thread(pthread_mutex_lock(&second->lock));
        if (job->from->units > 0) {
            job->from->units--;
            job->to->units++;
        }
        check_thread(pthread_mutex_unlock(&second->lock));
        check_thread(pthread_mutex_unlock(&first->lock));
    }
    return NULL;
}
int main(void) {
    struct Resource left = {10, 100, PTHREAD_MUTEX_INITIALIZER};
    struct Resource right = {20, 100, PTHREAD_MUTEX_INITIALIZER};
    struct Move jobs[2] = {{&left, &right}, {&right, &left}};
    pthread_t threads[2];
    for (size_t i = 0; i < 2; i++)
        check_thread(pthread_create(&threads[i], NULL, move_units, &jobs[i]));
    for (size_t i = 0; i < 2; i++)
        check_thread(pthread_join(threads[i], NULL));
    printf("left=%d right=%d total=%d\n", left.units, right.units,
           left.units + right.units);
    check_thread(pthread_mutex_destroy(&left.lock));
    check_thread(pthread_mutex_destroy(&right.lock));
    return 0;
}
