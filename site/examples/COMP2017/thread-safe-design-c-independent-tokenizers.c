// Leon | Original learning example
// Give concurrent parsers independent state
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

struct ParseJob {
    char text[16];
    int sum;
};
static void *parse(void *argument) {
    struct ParseJob *job = argument;
    char *save = NULL;
    char *token = strtok_r(job->text, ",", &save);
    while (token != NULL) {
        if (token[0] < '0' || token[0] > '9' || token[1] != '\0')
            exit(EXIT_FAILURE);
        job->sum += token[0] - '0';
        token = strtok_r(NULL, ",", &save);
    }
    return NULL;
}
int main(void) {
    struct ParseJob jobs[2] = {{{'1', ',', '2', ',', '3', '\0'}, 0},
                               {{'4', ',', '5', ',', '6', '\0'}, 0}};
    pthread_t threads[2];
    for (size_t i = 0; i < 2; i++)
        check_thread(pthread_create(&threads[i], NULL, parse, &jobs[i]));
    for (size_t i = 0; i < 2; i++)
        check_thread(pthread_join(threads[i], NULL));
    printf("first total=%d second total=%d\n", jobs[0].sum, jobs[1].sum);
    return 0;
}
