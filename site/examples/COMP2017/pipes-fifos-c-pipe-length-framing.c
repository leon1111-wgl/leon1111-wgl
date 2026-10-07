// Leon | Original learning example
// Reconstruct two length-prefixed frames
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
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
static int read_exact(int fd, void *data, size_t length) {
    unsigned char *bytes = data;
    size_t received = 0;
    while (received < length) {
        ssize_t amount = read(fd, bytes + received, length - received);
        if (amount == -1 && errno == EINTR)
            continue;
        if (amount < 0)
            return -1;
        if (amount == 0)
            return received == 0 ? 0 : -1;
        received += (size_t)amount;
    }
    return 1;
}

static int wait_child(pid_t child, int *status) {
    pid_t result;
    do {
        result = waitpid(child, status, 0);
    } while (result == -1 && errno == EINTR);
    return result == child;
}
int main(void) {
    int endpoints[2];
    if (pipe(endpoints) == -1)
        return 1;
    pid_t child = fork();
    if (child == -1) {
        close(endpoints[0]);
        close(endpoints[1]);
        return 1;
    }
    if (child == 0) {
        close(endpoints[0]);
        int ok = write_all(endpoints[1], "3cat4bird", 9);
        close(endpoints[1]);
        _exit(ok ? 0 : 1);
    }
    close(endpoints[1]);
    int valid = 1, frames = 0;
    for (;;) {
        char digit;
        int header = read_exact(endpoints[0], &digit, 1);
        if (header == 0)
            break;
        if (header < 0 || digit < '0' || digit > '8') {
            valid = 0;
            break;
        }
        size_t length = (size_t)(digit - '0');
        char payload[9];
        if (read_exact(endpoints[0], payload, length) != 1) {
            valid = 0;
            break;
        }
        payload[length] = '\0';
        printf("frame=%s\n", payload);
        frames++;
    }
    close(endpoints[0]);
    int status = 0;
    if (!wait_child(child, &status) || !WIFEXITED(status) || WEXITSTATUS(status) != 0 ||
        !valid)
        return 1;
    printf("frames=%d\n", frames);
    return 0;
}
