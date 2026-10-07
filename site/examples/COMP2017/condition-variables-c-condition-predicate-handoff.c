// Leon | Original learning example
// Publish one value through a protected predicate
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

static pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;
static pthread_cond_t changed = PTHREAD_COND_INITIALIZER;
static int ready = 0, payload = 0, consumed = 0;
static void *consume(void *argument) {
    (void)argument;
    check_thread(pthread_mutex_lock(&lock));
    while (!ready)
        check_thread(pthread_cond_wait(&changed, &lock));
    consumed = payload;
    check_thread(pthread_mutex_unlock(&lock));
    return NULL;
}
int main(void) {
    pthread_t thread;
    check_thread(pthread_create(&thread, NULL, consume, NULL));
    check_thread(pthread_mutex_lock(&lock));
    payload = 42;
    ready = 1;
    check_thread(pthread_cond_signal(&changed));
    check_thread(pthread_mutex_unlock(&lock));
    check_thread(pthread_join(thread, NULL));
    printf("consumed=%d\n", consumed);
    check_thread(pthread_cond_destroy(&changed));
    check_thread(pthread_mutex_destroy(&lock));
    return 0;
}
