// Leon | Original learning example
// Remove both a middle node and the head
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>

struct Node {
    int value;
    struct Node *next;
};
static int push(struct Node **head, int value) {
    struct Node *node = malloc(sizeof *node);
    if (node == NULL)
        return 0;
    node->value = value;
    node->next = *head;
    *head = node;
    return 1;
}
static void destroy(struct Node *node) {
    while (node != NULL) {
        struct Node *next = node->next;
        free(node);
        node = next;
    }
}
static void print_list(const struct Node *node) {
    for (; node != NULL; node = node->next)
        printf("%d -> ", node->value);
    puts("NULL");
}
static void remove_value(struct Node **head, int value) {
    struct Node **link = head;
    while (*link != NULL && (*link)->value != value)
        link = &(*link)->next;
    if (*link != NULL) {
        struct Node *victim = *link;
        *link = victim->next;
        free(victim);
    }
}
int main(void) {
    struct Node *head = NULL;
    if (!push(&head, 9) || !push(&head, 7) || !push(&head, 4)) {
        destroy(head);
        return 1;
    }
    print_list(head);
    remove_value(&head, 7);
    print_list(head);
    remove_value(&head, 4);
    print_list(head);
    destroy(head);
    return 0;
}
