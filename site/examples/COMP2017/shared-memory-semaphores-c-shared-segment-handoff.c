// Guoliang | Original learning example
// Observe explicit shared storage after a child completes
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <errno.h>
#include <sys/ipc.h>
#include <sys/shm.h>
static int wait_child(pid_t child, int *status) {
    pid_t result;
    do {
        result = waitpid(child, status, 0);
    } while (result == -1 && errno == EINTR);
    return result == child;
}
int main(void) {
    int segment = shmget(IPC_PRIVATE, sizeof(int), 0600);
    if (segment == -1)
        return 1;
    int *shared = shmat(segment, NULL, 0);
    if (shared == (void *)-1) {
        shmctl(segment, IPC_RMID, NULL);
        return 1;
    }
    if (shmctl(segment, IPC_RMID, NULL) == -1) {
        shmdt(shared);
        return 1;
    }
    *shared = 4;
    int local = 4;
    pid_t child = fork();
    if (child == -1) {
        shmdt(shared);
        return 1;
    }
    if (child == 0) {
        *shared = 17;
        local = 9;
        _exit(local == 9 ? 0 : 1);
    }
    int status = 0;
    if (!wait_child(child, &status) || !WIFEXITED(status) || WEXITSTATUS(status) != 0) {
        shmdt(shared);
        return 1;
    }
    printf("shared=%d parent local=%d\n", *shared, local);
    return shmdt(shared) == 0 ? 0 : 1;
}
