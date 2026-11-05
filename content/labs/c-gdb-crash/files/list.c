#include <stdlib.h>
#include <string.h>
#include "list.h"

/* Copy s into new heap storage; NULL in, NULL out. */
static char *copy_string(const char *s)
{
    if (s == NULL) {
        return NULL;
    }
    size_t n = strlen(s) + 1;
    char *p = malloc(n);
    if (p != NULL) {
        memcpy(p, s, n);
    }
    return p;
}

int list_add(Node **head, int id, const char *name)
{
    Node *node = malloc(sizeof *node);
    if (node == NULL) {
        return -1;
    }
    node->id = id;
    node->name = copy_string(name);
    node->next = NULL;

    Node **link = head;
    while (*link != NULL) {
        link = &(*link)->next;
    }
    *link = node;
    return 0;
}

Node *list_find_by_name(const Node *head, const char *wanted)
{
    for (const Node *node = head; node != NULL; node = node->next) {
        if (strcmp(node->name, wanted) == 0) {
            return (Node *)node;
        }
    }
    return NULL;
}

void list_free(Node *head)
{
    while (head != NULL) {
        Node *next = head->next;
        free(head->name);
        free(head);
        head = next;
    }
}
