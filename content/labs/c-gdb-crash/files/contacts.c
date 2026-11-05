#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "contacts.h"
#include "list.h"

/* Load "id,name,email" rows. An empty name field is stored as NULL. */
int contacts_load(const char *path, Node **head)
{
    FILE *fp = fopen(path, "r");
    if (fp == NULL) {
        return -1;
    }
    char line[128];
    int row = 0;
    while (fgets(line, sizeof line, fp) != NULL) {
        row++;
        char *id_end = strchr(line, ',');
        if (id_end == NULL) {
            fprintf(stderr, "%s:%d: malformed row\n", path, row);
            continue;
        }
        char *name_start = id_end + 1;
        char *name_end = strchr(name_start, ',');
        if (name_end == NULL) {
            fprintf(stderr, "%s:%d: malformed row\n", path, row);
            continue;
        }
        *name_end = '\0';
        int id = atoi(line);
        const char *name = (name_end == name_start) ? NULL : name_start;
        list_add(head, id, name);
    }
    fclose(fp);
    return 0;
}
