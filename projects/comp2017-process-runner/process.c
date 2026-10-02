/* Guoliang | Original teaching project. */
#include "process.h"

#include <errno.h>
#include <fcntl.h>
#include <signal.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

/* Child failure: no stdio flushing or parent atexit handlers after fork. */
static void child_failure(const char *message, size_t length, int code)
{
    while (length > 0) {
        ssize_t sent = write(STDERR_FILENO, message, length);
        if (sent < 0 && errno == EINTR) {
            continue;
        }
        if (sent <= 0) {
            break;
        }
        message += (size_t)sent;
        length -= (size_t)sent;
    }
    _exit(code);
}

static void execute_child(int read_end, int write_end, char *const argv[])
{
    static const char setup_error[] = "process_runner: stdout setup failed\n";
    static const char exec_error[] = "process_runner: execvp failed\n";
    (void)close(read_end);
    int copied;
    do {
        copied = dup2(write_end, STDOUT_FILENO);
    } while (copied == -1 && errno == EINTR);
    if (copied == -1) {
        (void)close(write_end);
        child_failure(setup_error, sizeof(setup_error) - 1, 126);
    }
    (void)close(write_end);
    /* The original argument boundaries survive; no command string is built. */
    execvp(argv[0], argv);
    child_failure(exec_error, sizeof(exec_error) - 1, 127);
}

static int drain_output(int read_end, unsigned char *buffer, size_t capacity,
                        struct process_result *result)
{
    unsigned char chunk[4096];
    for (;;) {
        ssize_t received = read(read_end, chunk, sizeof(chunk));
        if (received == -1 && errno == EINTR) {
            continue;
        }
        if (received == -1) {
            return -1;
        }
        if (received == 0) {
            return 0;
        }
        size_t count = (size_t)received;
        size_t space = capacity - result->captured;
        size_t keep = count < space ? count : space;
        if (keep > 0) {
            memcpy(buffer + result->captured, chunk, keep);
            result->captured += keep;
        }
        if (keep < count) {
            result->truncated = true;
        }
        /* A full buffer stops copying, never reading. The child must progress. */
    }
}

int process_run(char *const argv[], unsigned char *buffer, size_t capacity,
                struct process_result *result)
{
    if (argv == NULL || argv[0] == NULL || argv[0][0] == '\0' ||
        result == NULL || capacity > PROCESS_MAX_CAPTURE ||
        (capacity > 0 && buffer == NULL)) {
        errno = EINVAL;
        return -1;
    }
    /* Keeps both pipe descriptors above 2, so dup2/close ownership is simple. */
    for (int fd = STDIN_FILENO; fd <= STDERR_FILENO; ++fd) {
        if (fcntl(fd, F_GETFD) == -1) {
            return -1;
        }
    }
    *result = (struct process_result){0, false, 0};
    int channel[2];
    if (pipe(channel) == -1) {
        return -1;
    }
    pid_t child = fork();
    if (child == -1) {
        int saved = errno;
        (void)close(channel[0]);
        (void)close(channel[1]);
        errno = saved;
        return -1;
    }
    if (child == 0) {
        execute_child(channel[0], channel[1], argv);
    }
    /* Parent owns only the read end. Keeping any write end would prevent EOF. */
    (void)close(channel[1]);
    int failure = 0;
    if (drain_output(channel[0], buffer, capacity, result) == -1) {
        failure = errno;
        /* On a read error, abort our direct child before trying to reap it. */
        (void)kill(child, SIGKILL);
    }
    (void)close(channel[0]);
    pid_t waited;
    do {
        waited = waitpid(child, &result->wait_status, 0);
    } while (waited == -1 && errno == EINTR);
    if (waited == -1 && failure == 0) {
        failure = errno;
    }
    if (failure != 0) {
        errno = failure;
        return -1;
    }
    return 0;
}
