#ifndef LIST_H
#define LIST_H

/* One contact in a singly linked list. */
typedef struct node {
    int id;
    char *name;             /* owned copy of the name */
    struct node *next;
} Node;

/* Append a contact to the end of the list. Returns 0 on success, -1 on error. */
int list_add(Node **head, int id, const char *name);

/* Return the first node whose name equals wanted, or NULL. */
Node *list_find_by_name(const Node *head, const char *wanted);

void list_free(Node *head);

#endif
