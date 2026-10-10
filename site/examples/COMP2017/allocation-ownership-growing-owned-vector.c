// Leon | Original learning example
// Grow an owned array without losing it
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
struct Vector { int *data; size_t length; size_t capacity; };
static int reserve(struct Vector *v, size_t need) {
    const size_t limit = SIZE_MAX / sizeof *v->data;
    if (need <= v->capacity) return 1;
    if (need > limit) return 0;
    size_t next = v->capacity ? v->capacity : 2;
    while (next < need) {
        if (next > limit / 2) { next = need; break; }
        next *= 2;
    }
    int *temporary = realloc(v->data, next * sizeof *v->data);
    if (temporary == NULL) return 0;
    v->data = temporary;
    v->capacity = next;
    return 1;
}
static int push(struct Vector *v, int value) {
    if (v->length == SIZE_MAX || !reserve(v, v->length + 1)) return 0;
    v->data[v->length++] = value;
    return 1;
}
static void destroy(struct Vector *v) {
    free(v->data);
    *v = (struct Vector){0};
}
int main(void) {
    struct Vector values = {0};
    for (int n = 1; n <= 5; ++n) {
        if (!push(&values, n * 10)) { destroy(&values); return 1; }
        printf("length=%zu capacity=%zu\n", values.length, values.capacity);
    }
    int rejected = !reserve(&values, SIZE_MAX);
    assert(rejected && values.length == 5 && values.data[0] == 10);
    printf("oversized request rejected: %d\n", rejected);
    printf("last value: %d\n", values.data[values.length - 1]);
    destroy(&values);
    assert(values.data == NULL && values.length == 0 && values.capacity == 0);
    puts("owner reset after free");
    return 0;
}
