// Guoliang | Original learning example
// Change two copies of ordinary state
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <errno.h>
static int wait_child(pid_t child, int *status) {
    pid_t result;
    do {
        result = waitpid(child, status, 0);
    } while (result == -1 && errno == EINTR);
    return result == child;
}
int main(void) {
    int value = 5;
    pid_t child = fork();
    if (child == -1)
        return 1;
    if (child == 0) {
        value = 12;
        _exit(value);
    }
    value = 8;
    int status = 0;
    if (!wait_child(child, &status) || !WIFEXITED(status))
        return 1;
    printf("parent value=%d\n", value);
    printf("child reported=%d\n", WEXITSTATUS(status));
    return 0;
}
