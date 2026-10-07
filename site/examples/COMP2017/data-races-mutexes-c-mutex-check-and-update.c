// Leon | Original learning example
// Protect the complete final-item transaction
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
static int stock = 1;
struct Attempt {
    int success;
};
static void *sell(void *argument) {
    struct Attempt *attempt = argument;
    check_thread(pthread_mutex_lock(&lock));
    if (stock > 0) {
        stock--;
        attempt->success = 1;
    }
    check_thread(pthread_mutex_unlock(&lock));
    return NULL;
}
int main(void) {
    struct Attempt attempts[2] = {{0}, {0}};
    pthread_t threads[2];
    for (size_t i = 0; i < 2; i++)
        check_thread(pthread_create(&threads[i], NULL, sell, &attempts[i]));
    for (size_t i = 0; i < 2; i++)
        check_thread(pthread_join(threads[i], NULL));
    printf("successful requests=%d\n", attempts[0].success + attempts[1].success);
    printf("remaining stock=%d\n", stock);
    check_thread(pthread_mutex_destroy(&lock));
    return 0;
}
