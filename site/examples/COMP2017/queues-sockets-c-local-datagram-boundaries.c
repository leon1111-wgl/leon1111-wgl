// Leon | Original learning example
// Preserve two local datagram boundaries
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/socket.h>

int main(void) {
    int sockets[2];
    if (socketpair(AF_UNIX, SOCK_DGRAM, 0, sockets) == -1)
        return 1;
    if (send(sockets[0], "cat", 3, 0) != 3 || send(sockets[0], "bird", 4, 0) != 4) {
        close(sockets[0]);
        close(sockets[1]);
        return 1;
    }
    for (int i = 0; i < 2; i++) {
        char payload[16];
        ssize_t length = recv(sockets[1], payload, sizeof payload, 0);
        if (length < 0) {
            close(sockets[0]);
            close(sockets[1]);
            return 1;
        }
        printf("datagram %d bytes=%zd text=%.*s\n", i, length, (int)length, payload);
    }
    int first = close(sockets[0]);
    int second = close(sockets[1]);
    return first == 0 && second == 0 ? 0 : 1;
}
