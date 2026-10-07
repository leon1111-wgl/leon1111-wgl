// Leon | Original learning example
// Drain a bounded queue and then shut down
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

enum { CAPACITY = 2 };
static int buffer[CAPACITY];
static size_t head = 0, tail = 0, count = 0;
static int closed = 0, received = 0, total = 0;
static pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;
static pthread_cond_t not_empty = PTHREAD_COND_INITIALIZER;
static pthread_cond_t not_full = PTHREAD_COND_INITIALIZER;
static void *producer(void *argument) {
    (void)argument;
    for (int value = 1; value <= 5; value++) {
        check_thread(pthread_mutex_lock(&lock));
        while (count == CAPACITY)
            check_thread(pthread_cond_wait(&not_full, &lock));
        buffer[tail] = value;
        tail = (tail + 1) % CAPACITY;
        count++;
        check_thread(pthread_cond_signal(&not_empty));
        check_thread(pthread_mutex_unlock(&lock));
    }
    check_thread(pthread_mutex_lock(&lock));
    closed = 1;
    check_thread(pthread_cond_broadcast(&not_empty));
    check_thread(pthread_mutex_unlock(&lock));
    return NULL;
}
static void *consumer(void *argument) {
    (void)argument;
    for (;;) {
        check_thread(pthread_mutex_lock(&lock));
        while (count == 0 && !closed)
            check_thread(pthread_cond_wait(&not_empty, &lock));
        if (count == 0 && closed) {
            check_thread(pthread_mutex_unlock(&lock));
            break;
        }
        int value = buffer[head];
        head = (head + 1) % CAPACITY;
        count--;
        check_thread(pthread_cond_signal(&not_full));
        check_thread(pthread_mutex_unlock(&lock));
        total += value;
        received++;
    }
    return NULL;
}
int main(void) {
    pthread_t producer_thread, consumer_thread;
    check_thread(pthread_create(&consumer_thread, NULL, consumer, NULL));
    check_thread(pthread_create(&producer_thread, NULL, producer, NULL));
    check_thread(pthread_join(producer_thread, NULL));
    check_thread(pthread_join(consumer_thread, NULL));
    printf("consumed=%d sum=%d\n", received, total);
    printf("remaining=%zu closed=%d\n", count, closed);
    check_thread(pthread_cond_destroy(&not_empty));
    check_thread(pthread_cond_destroy(&not_full));
    check_thread(pthread_mutex_destroy(&lock));
    return 0;
}
