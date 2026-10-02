// Guoliang | Original learning example
// Handle an exec failure without duplicating buffers
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
    pid_t child = fork();
    if (child == -1)
        return 1;
    if (child == 0) {
        char *arguments[] = {"unused", NULL};
        execv("", arguments);
        _exit(127);
    }
    int status = 0;
    if (!wait_child(child, &status))
        return 1;
    if (WIFEXITED(status))
        printf("launcher failure status=%d\n", WEXITSTATUS(status));
    else
        return 1;
    return 0;
}
