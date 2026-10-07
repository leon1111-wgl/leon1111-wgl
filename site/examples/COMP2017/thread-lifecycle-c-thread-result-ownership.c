// Leon | Original learning example
// Transfer a heap result through join
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

static void *worker(void *argument) {
    int input = *(int *)argument;
    free(argument);
    int *result = malloc(sizeof *result);
    if (result == NULL)
        return NULL;
    *result = input * input;
    return result;
}
int main(void) {
    int *argument = malloc(sizeof *argument);
    if (argument == NULL)
        return 1;
    *argument = 7;
    pthread_t thread;
    int error = pthread_create(&thread, NULL, worker, argument);
    if (error != 0) {
        free(argument);
        return 1;
    }
    void *raw_result = NULL;
    check_thread(pthread_join(thread, &raw_result));
    if (raw_result == NULL)
        return 1;
    int *result = raw_result;
    printf("result=%d\n", *result);
    free(result);
    puts("result released by joiner");
    return 0;
}
