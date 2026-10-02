// Guoliang | Original learning example
// Before threads: understand the queue state
#include <stdio.h>
#include <stdlib.h>
enum { CAPACITY = 2 };
struct Queue {
    int data[CAPACITY];
    size_t head, tail, count;
};
static int push(struct Queue *q, int value) {
    if (q->count == CAPACITY)
        return 0;
    q->data[q->tail] = value;
    q->tail = (q->tail + 1) % CAPACITY;
    q->count++;
    return 1;
}
static int pop(struct Queue *q, int *value) {
    if (q->count == 0)
        return 0;
    *value = q->data[q->head];
    q->head = (q->head + 1) % CAPACITY;
    q->count--;
    return 1;
}
static void show(const struct Queue *q) {
    printf("head=%zu tail=%zu count=%zu\n", q->head, q->tail, q->count);
}
int main(void) {
    struct Queue q = {{0}, 0, 0, 0};
    int value = -1;
    printf("push 10=%d\n", push(&q, 10));
    printf("push 20=%d\n", push(&q, 20));
    show(&q);
    printf("push full=%d\n", push(&q, 30));
    if (pop(&q, &value))
        printf("pop=%d\n", value);
    printf("push 30=%d\n", push(&q, 30));
    show(&q);
    while (pop(&q, &value))
        printf("pop=%d\n", value);
    show(&q);
    return 0;
}
