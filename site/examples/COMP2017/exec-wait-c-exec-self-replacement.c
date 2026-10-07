// Leon | Original learning example
// Replace a child with a fresh copy of this program
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <errno.h>
#include <string.h>
static int wait_child(pid_t child, int *status) {
    pid_t result;
    do {
        result = waitpid(child, status, 0);
    } while (result == -1 && errno == EINTR);
    return result == child;
}
int main(int argc, char **argv) {
    if (argc == 2 && strcmp(argv[1], "child") == 0) {
        puts("replacement image running");
        return 7;
    }
    if (argc < 1 || argv[0] == NULL || argv[0][0] == '\0')
        return 1;
    pid_t child = fork();
    if (child == -1)
        return 1;
    if (child == 0) {
        execl(argv[0], argv[0], "child", (char *)NULL);
        _exit(127);
    }
    int status = 0;
    if (!wait_child(child, &status) || !WIFEXITED(status))
        return 1;
    printf("replacement exit=%d\n", WEXITSTATUS(status));
    return 0;
}
