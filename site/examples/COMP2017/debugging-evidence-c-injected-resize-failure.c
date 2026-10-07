// Leon | Original learning example
// Inject allocation failure and verify preserved ownership
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
struct Buffer {
    int *data;
    size_t length;
    size_t capacity;
};
typedef void *(*Resize)(void *, size_t);
static void *fail_resize(void *old, size_t size) {
    (void)old;
    (void)size;
    return NULL;
}
static int append(struct Buffer *buffer, int value, Resize resize) {
    if (buffer->length == buffer->capacity) {
        if (buffer->capacity > SIZE_MAX / 2)
            return 0;
        size_t capacity = buffer->capacity ? buffer->capacity * 2 : 1;
        if (capacity > SIZE_MAX / sizeof *buffer->data)
            return 0;
        int *next = resize(buffer->data, capacity * sizeof *buffer->data);
        if (next == NULL)
            return 0;
        buffer->data = next;
        buffer->capacity = capacity;
    }
    buffer->data[buffer->length++] = value;
    return 1;
}
int main(void) {
    struct Buffer buffer = {malloc(2 * sizeof(int)), 2, 2};
    if (buffer.data == NULL)
        return 1;
    buffer.data[0] = 4;
    buffer.data[1] = 7;
    int failed = append(&buffer, 9, fail_resize);
    printf("injected accepted=%d length=%zu capacity=%zu values=%d,%d\n", failed,
           buffer.length, buffer.capacity, buffer.data[0], buffer.data[1]);
    int accepted = append(&buffer, 9, realloc);
    if (!accepted) {
        free(buffer.data);
        return 1;
    }
    printf("real accepted=%d length=%zu capacity=%zu values=%d,%d,%d\n", accepted,
           buffer.length, buffer.capacity, buffer.data[0], buffer.data[1],
           buffer.data[2]);
    free(buffer.data);
    return 0;
}
