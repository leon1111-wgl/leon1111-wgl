#include <stdio.h>
#include "contacts.h"
#include "list.h"

int main(int argc, char **argv)
{
    if (argc < 3) {
        fprintf(stderr, "usage: %s contacts.csv name...\n", argv[0]);
        return 2;
    }
    Node *head = NULL;
    if (contacts_load(argv[1], &head) != 0) {
        perror(argv[1]);
        return 1;
    }
    for (int i = 2; i < argc; i++) {
        const Node *hit = list_find_by_name(head, argv[i]);
        if (hit != NULL) {
            printf("%s -> id %d\n", argv[i], hit->id);
        } else {
            printf("%s -> not found\n", argv[i]);
        }
        fflush(stdout);         /* a crash must not swallow earlier results */
    }
    list_free(head);
    return 0;
}
