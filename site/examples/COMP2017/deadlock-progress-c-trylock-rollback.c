// Leon | Original learning example
// Release a partial acquisition after a failed try
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <string.h>
#include <errno.h>
static void check_thread(int code) {
    if (code != 0) {
        fprintf(stderr, "pthread error: %s\n", strerror(code));
        exit(EXIT_FAILURE);
    }
}

static pthread_mutex_t first = PTHREAD_MUTEX_INITIALIZER;
static pthread_mutex_t second = PTHREAD_MUTEX_INITIALIZER;
static int rolled_back = 0;
static void *attempt(void *argument) {
    (void)argument;
    check_thread(pthread_mutex_lock(&first));
    int result = pthread_mutex_trylock(&second);
    if (result == EBUSY) {
        check_thread(pthread_mutex_unlock(&first));
        rolled_back = 1;
        return NULL;
    }
    check_thread(result);
    check_thread(pthread_mutex_unlock(&second));
    check_thread(pthread_mutex_unlock(&first));
    return NULL;
}
int main(void) {
    check_thread(pthread_mutex_lock(&second));
    pthread_t thread;
    check_thread(pthread_create(&thread, NULL, attempt, NULL));
    check_thread(pthread_join(thread, NULL));
    check_thread(pthread_mutex_unlock(&second));
    check_thread(pthread_mutex_trylock(&first));
    puts("first lock available after rollback");
    check_thread(pthread_mutex_unlock(&first));
    printf("busy path taken=%d\n", rolled_back);
    check_thread(pthread_mutex_destroy(&first));
    check_thread(pthread_mutex_destroy(&second));
    return 0;
}
