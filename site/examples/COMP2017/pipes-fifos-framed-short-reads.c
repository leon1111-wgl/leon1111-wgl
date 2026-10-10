// Leon | Original learning example
// Read a complete frame from a byte stream
#define _POSIX_C_SOURCE 200809L
#include <assert.h>
#include <errno.h>
#include <stdio.h>
#include <unistd.h>
enum Result { COMPLETE, CLEAN_EOF, TRUNCATED, IO_ERROR };
static enum Result read_exact(int fd, unsigned char *out, size_t need) {
    size_t used = 0;
    while (used < need) {
        size_t request = need - used;
        if (request > 2) request = 2; /* Deliberately fragment reads. */
        ssize_t n = read(fd, out + used, request);
        if (n > 0) { used += (size_t)n; continue; }
        if (n == 0) return used == 0 ? CLEAN_EOF : TRUNCATED;
        if (errno == EINTR) continue;
        return IO_ERROR;
    }
    return COMPLETE;
}
static int write_all(int fd, const unsigned char *data, size_t size) {
    size_t sent = 0;
    while (sent < size) {
        ssize_t n = write(fd, data + sent, size - sent);
        if (n > 0) sent += (size_t)n;
        else if (n < 0 && errno == EINTR) continue;
        else return 0;
    }
    return 1;
}
int main(void) {
    int channel[2];
    if (pipe(channel) == -1) return 1;
    const unsigned char wire[] = {4, 'p', 'i', 'n', 'g', 3, 'o', 'k'};
    int sent = write_all(channel[1], wire, sizeof wire);
    int closed = close(channel[1]);
    if (!sent || closed == -1) { close(channel[0]); return 1; }
    unsigned char length, payload[16];
    enum Result header = read_exact(channel[0], &length, 1);
    if (header != COMPLETE || length == 0 || length > sizeof payload) {
        close(channel[0]); return 1;
    }
    enum Result body = read_exact(channel[0], payload, length);
    if (body != COMPLETE) { close(channel[0]); return 1; }
    printf("frame: %.*s\n", (int)length, (char *)payload);
    header = read_exact(channel[0], &length, 1);
    if (header != COMPLETE || length == 0 || length > sizeof payload) {
        close(channel[0]); return 1;
    }
    body = read_exact(channel[0], payload, length);
    assert(body == TRUNCATED);
    puts("second frame: truncated payload");
    enum Result end = read_exact(channel[0], &length, 1);
    assert(end == CLEAN_EOF);
    puts("next header: clean EOF");
    return close(channel[0]) == 0 ? 0 : 1;
}
