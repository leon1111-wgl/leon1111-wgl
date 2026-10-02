// Guoliang | Original learning example
// Record a signal and handle it in normal flow
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
static volatile sig_atomic_t requested = 0;
static void record_request(int signal_number) {
    (void)signal_number;
    requested = 1;
}
int main(void) {
    struct sigaction action = {0};
    struct sigaction previous;
    action.sa_handler = record_request;
    if (sigemptyset(&action.sa_mask) == -1)
        return 1;
    if (sigaction(SIGUSR1, &action, &previous) == -1)
        return 1;
    if (raise(SIGUSR1) != 0)
        return 1;
    printf("request observed=%s\n", requested ? "yes" : "no");
    puts("cleanup in normal flow");
    if (sigaction(SIGUSR1, &previous, NULL) == -1)
        return 1;
    return 0;
}
