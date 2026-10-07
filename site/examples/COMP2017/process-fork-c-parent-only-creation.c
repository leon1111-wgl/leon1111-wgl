// Leon | Original learning example
// Count a parent-only creation loop
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
    int created = 0, status_sum = 0;
    for (int i = 0; i < 3; i++) {
        pid_t child = fork();
        if (child == -1)
            return 1;
        if (child == 0)
            _exit(i + 1);
        int status = 0;
        if (!wait_child(child, &status) || !WIFEXITED(status))
            return 1;
        created++;
        status_sum += WEXITSTATUS(status);
    }
    printf("children created=%d\n", created);
    printf("distinct processes=%d\n", created + 1);
    printf("status sum=%d\n", status_sum);
    return 0;
}
