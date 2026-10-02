// Guoliang | Original learning example
// Consume and return semaphore permits
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <semaphore.h>
#include <errno.h>

int main(void) {
    char name[64];
    int length = snprintf(name, sizeof name, "/glv3-%ld", (long)getpid());
    if (length < 0 || (size_t)length >= sizeof name)
        return 1;
    sem_t *permits = sem_open(name, O_CREAT | O_EXCL, 0600, 2);
    if (permits == SEM_FAILED)
        return 1;
    if (sem_unlink(name) == -1) {
        sem_close(permits);
        return 1;
    }
    if (sem_trywait(permits) == -1 || sem_trywait(permits) == -1) {
        sem_close(permits);
        return 1;
    }
    puts("two permits acquired");
    errno = 0;
    if (sem_trywait(permits) != -1 || errno != EAGAIN) {
        sem_close(permits);
        return 1;
    }
    puts("third request has no permit");
    if (sem_post(permits) == -1 || sem_trywait(permits) == -1) {
        sem_close(permits);
        return 1;
    }
    puts("returned permit acquired again");
    return sem_close(permits) == 0 ? 0 : 1;
}
