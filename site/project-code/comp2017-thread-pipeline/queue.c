/* Guoliang | Original teaching project. */
#include "queue.h"

#include <stdio.h>
#include <stdlib.h>

void thread_check(int error, const char *operation) {
    if (error != 0) {
        fprintf(stderr, "fatal: %s failed (pthread error %d)\n", operation, error);
        /* Continuing could access unprotected data or strand a waiter.
           This teaching policy exits the process, without orderly cleanup. */
        exit(EXIT_FAILURE);
    }
}

int queue_init(WorkQueue *queue) {
    queue->head = 0;
    queue->count = 0;
    queue->closed = false;
    int error = pthread_mutex_init(&queue->mutex, NULL);
    if (error != 0) {
        return error;
    }
    error = pthread_cond_init(&queue->not_empty, NULL);
    if (error != 0) {
        thread_check(pthread_mutex_destroy(&queue->mutex), "mutex destroy");
        return error;
    }
    error = pthread_cond_init(&queue->not_full, NULL);
    if (error != 0) {
        thread_check(pthread_cond_destroy(&queue->not_empty), "condition destroy");
        thread_check(pthread_mutex_destroy(&queue->mutex), "mutex destroy");
    }
    return error;
}

bool queue_push(WorkQueue *queue, size_t job) {
    thread_check(pthread_mutex_lock(&queue->mutex), "mutex lock");
    while (queue->count == QUEUE_CAPACITY && !queue->closed) {
        thread_check(pthread_cond_wait(&queue->not_full, &queue->mutex),
                     "wait not_full");
    }
    if (queue->closed) {
        thread_check(pthread_mutex_unlock(&queue->mutex), "mutex unlock");
        return false;
    }
    size_t tail = (queue->head + queue->count) % QUEUE_CAPACITY;
    queue->entries[tail] = job;
    queue->count++;
    thread_check(pthread_cond_signal(&queue->not_empty), "signal not_empty");
    thread_check(pthread_mutex_unlock(&queue->mutex), "mutex unlock");
    return true;
}

bool queue_pop(WorkQueue *queue, size_t *job) {
    thread_check(pthread_mutex_lock(&queue->mutex), "mutex lock");
    while (queue->count == 0 && !queue->closed) {
        thread_check(pthread_cond_wait(&queue->not_empty, &queue->mutex),
                     "wait not_empty");
    }
    if (queue->count == 0) {
        thread_check(pthread_mutex_unlock(&queue->mutex), "mutex unlock");
        return false;
    }
    *job = queue->entries[queue->head];
    queue->head = (queue->head + 1) % QUEUE_CAPACITY;
    queue->count--;
    thread_check(pthread_cond_signal(&queue->not_full), "signal not_full");
    thread_check(pthread_mutex_unlock(&queue->mutex), "mutex unlock");
    return true;
}

void queue_close(WorkQueue *queue) {
    thread_check(pthread_mutex_lock(&queue->mutex), "mutex lock");
    queue->closed = true;
    /* All empty-queue consumers must learn that no future job can arrive. */
    thread_check(pthread_cond_broadcast(&queue->not_empty), "broadcast not_empty");
    thread_check(pthread_cond_broadcast(&queue->not_full), "broadcast not_full");
    thread_check(pthread_mutex_unlock(&queue->mutex), "mutex unlock");
}

void queue_destroy(WorkQueue *queue) {
    thread_check(pthread_cond_destroy(&queue->not_full), "condition destroy");
    thread_check(pthread_cond_destroy(&queue->not_empty), "condition destroy");
    thread_check(pthread_mutex_destroy(&queue->mutex), "mutex destroy");
}
