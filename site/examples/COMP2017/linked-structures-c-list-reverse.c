// Guoliang | Original learning example
// Reverse links without losing the suffix
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>

struct Node {
    int value;
    struct Node *next;
};
int main(void) {
    struct Node third = {9, NULL};
    struct Node second = {7, &third};
    struct Node first = {4, &second};
    struct Node *head = &first;
    struct Node *previous = NULL;
    while (head != NULL) {
        struct Node *next = head->next;
        head->next = previous;
        previous = head;
        head = next;
    }
    head = previous;
    for (const struct Node *node = head; node != NULL; node = node->next)
        printf("%d -> ", node->value);
    puts("NULL");
    return 0;
}
