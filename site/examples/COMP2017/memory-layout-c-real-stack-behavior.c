// Leon | Original learning example
// Watch real frames and keep recursion inside a budget
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

#define LEVELS 4
static uintptr_t where[2][LEVELS];

/* Remember the address of one local variable at each call depth. */
static void descend(int round, int level) {
    char marker = 0;
    where[round][level] = (uintptr_t)&marker;
    if (level + 1 < LEVELS)
        descend(round, level + 1);
}

/* Recursion with a depth budget: refuse instead of running out of stack. */
static long sum_to(long n, int depth, int limit) {
    if (depth > limit)
        return -1;
    if (n == 0)
        return 0;
    long rest = sum_to(n - 1, depth + 1, limit);
    if (rest < 0)
        return -1;
    return n + rest;
}

int main(void) {
    descend(0, 0);
    descend(1, 0);

    int lower = 1;
    for (int level = 1; level < LEVELS; level++)
        if (where[0][level] >= where[0][level - 1])
            lower = 0;
    printf("each deeper call has a lower local address: %s\n", lower ? "yes" : "no");

    int same = 1;
    for (int level = 0; level < LEVELS; level++)
        if (where[0][level] != where[1][level])
            same = 0;
    printf("a second round reuses the same addresses: %s\n", same ? "yes" : "no");

    void *block = malloc(100);
    int apart = block != NULL;
    for (int level = 0; level < LEVELS; level++)
        if ((uintptr_t)block == where[0][level])
            apart = 0;
    printf("heap block differs from every frame address: %s\n", apart ? "yes" : "no");
    free(block);

    printf("sum_to(10) with budget 100 = %ld\n", sum_to(10, 0, 100));
    printf("sum_to(5000) with budget 100 = %ld\n", sum_to(5000, 0, 100));

    size_t stack_bytes = 8u * 1024u * 1024u;
    size_t frame_bytes = 48;
    printf("an %zu byte stack holds about %zu frames of %zu bytes\n",
           stack_bytes, stack_bytes / frame_bytes, frame_bytes);
    size_t array_bytes = 3000000u * sizeof(int);
    printf("a local int[3000000] needs %zu bytes: %s\n", array_bytes,
           array_bytes > stack_bytes ? "too big for the stack, use malloc" : "fits");
    return 0;
}
