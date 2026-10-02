// Guoliang | Original learning example
// Accept a pending signal synchronously
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>

int main(void) {
    sigset_t selected, previous, pending;
    if (sigemptyset(&selected) == -1 || sigaddset(&selected, SIGUSR1) == -1)
        return 1;
    if (sigprocmask(SIG_BLOCK, &selected, &previous) == -1)
        return 1;
    if (raise(SIGUSR1) != 0)
        return 1;
    if (sigpending(&pending) == -1)
        return 1;
    int member = sigismember(&pending, SIGUSR1);
    if (member == -1)
        return 1;
    printf("pending before wait=%s\n", member ? "yes" : "no");
    int received = 0;
    if (sigwait(&selected, &received) != 0)
        return 1;
    printf("accepted expected signal=%s\n", received == SIGUSR1 ? "yes" : "no");
    if (sigprocmask(SIG_SETMASK, &previous, NULL) == -1)
        return 1;
    return 0;
}
