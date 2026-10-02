// Guoliang | Original learning example
// Drain a pipe after closing the writer
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
static int write_all(int fd, const void *data, size_t length) {
    const unsigned char *bytes = data;
    size_t sent = 0;
    while (sent < length) {
        ssize_t amount = write(fd, bytes + sent, length - sent);
        if (amount == -1 && errno == EINTR)
            continue;
        if (amount <= 0)
            return 0;
        sent += (size_t)amount;
    }
    return 1;
}
int main(void) {
    int endpoints[2];
    if (pipe(endpoints) == -1)
        return 1;
    const char message[] = "hello";
    if (!write_all(endpoints[1], message, 5)) {
        close(endpoints[0]);
        close(endpoints[1]);
        return 1;
    }
    if (close(endpoints[1]) == -1) {
        close(endpoints[0]);
        return 1;
    }
    char result[6];
    size_t total = 0;
    for (;;) {
        char chunk[2];
        ssize_t amount = read(endpoints[0], chunk, sizeof chunk);
        if (amount == -1 && errno == EINTR)
            continue;
        if (amount < 0) {
            close(endpoints[0]);
            return 1;
        }
        if (amount == 0)
            break;
        if ((size_t)amount > 5 - total) {
            close(endpoints[0]);
            return 1;
        }
        for (ssize_t i = 0; i < amount; i++)
            result[total++] = chunk[i];
    }
    result[total] = '\0';
    printf("received=%s bytes=%zu\n", result, total);
    puts("EOF after writer closed");
    return close(endpoints[0]) == 0 ? 0 : 1;
}
