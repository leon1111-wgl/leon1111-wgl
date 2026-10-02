// Guoliang | Original learning example
// Send only the defined payload bytes
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/msg.h>
struct Message {
    long type;
    char payload[16];
};
int main(void) {
    int queue = msgget(IPC_PRIVATE, 0600);
    if (queue == -1)
        return 1;
    struct Message sent = {2, {'h', 'e', 'l', 'l', 'o'}};
    if (msgsnd(queue, &sent, 5, IPC_NOWAIT) == -1) {
        msgctl(queue, IPC_RMID, NULL);
        return 1;
    }
    struct Message received = {0, {0}};
    ssize_t length = msgrcv(queue, &received, sizeof received.payload, 2, IPC_NOWAIT);
    if (length == -1) {
        msgctl(queue, IPC_RMID, NULL);
        return 1;
    }
    printf("type=%ld bytes=%zd text=%.*s\n", received.type, length, (int)length,
           received.payload);
    if (msgctl(queue, IPC_RMID, NULL) == -1)
        return 1;
    puts("queue removed");
    return 0;
}
