// Guoliang | Original learning example
// Return copies from a protected configuration
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

static pthread_rwlock_t lock = PTHREAD_RWLOCK_INITIALIZER;
static char configuration[16] = "blue";
struct Snapshot {
    char text[16];
};
static void *copy_configuration(void *argument) {
    struct Snapshot *snapshot = argument;
    check_thread(pthread_rwlock_rdlock(&lock));
    strcpy(snapshot->text, configuration);
    check_thread(pthread_rwlock_unlock(&lock));
    return NULL;
}
int main(void) {
    struct Snapshot snapshots[2] = {{{0}}, {{0}}};
    pthread_t readers[2];
    for (size_t i = 0; i < 2; i++)
        check_thread(
            pthread_create(&readers[i], NULL, copy_configuration, &snapshots[i]));
    for (size_t i = 0; i < 2; i++)
        check_thread(pthread_join(readers[i], NULL));
    check_thread(pthread_rwlock_wrlock(&lock));
    strcpy(configuration, "green");
    check_thread(pthread_rwlock_unlock(&lock));
    printf("first snapshot=%s second snapshot=%s\n", snapshots[0].text,
           snapshots[1].text);
    check_thread(pthread_rwlock_rdlock(&lock));
    printf("current=%s\n", configuration);
    check_thread(pthread_rwlock_unlock(&lock));
    check_thread(pthread_rwlock_destroy(&lock));
    return 0;
}
