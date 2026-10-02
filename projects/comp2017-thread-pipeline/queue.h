/* Guoliang | Original teaching project. */
#ifndef QUEUE_H
#define QUEUE_H

#include <pthread.h>
#include <stdbool.h>
#include <stddef.h>

#define QUEUE_CAPACITY 4u

/* Queue entries are job indices, not owning pointers. Protect all fields
   after initialization with mutex. Destroy only after every worker joins. */
typedef struct {
    size_t entries[QUEUE_CAPACITY];
    size_t head;
    size_t count;
    bool closed;
    pthread_mutex_t mutex;
    pthread_cond_t not_empty;
    pthread_cond_t not_full;
} WorkQueue;

/* Runtime synchronization failures terminate the process; see README. */
void thread_check(int error, const char *operation);
int queue_init(WorkQueue *queue);
bool queue_push(WorkQueue *queue, size_t job);
bool queue_pop(WorkQueue *queue, size_t *job);
void queue_close(WorkQueue *queue);
void queue_destroy(WorkQueue *queue);

#endif
