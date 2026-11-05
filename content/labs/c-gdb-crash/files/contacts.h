#ifndef CONTACTS_H
#define CONTACTS_H

#include "list.h"

/* Read a CSV file into the list. Returns 0, or -1 if the file cannot be opened. */
int contacts_load(const char *path, Node **head);

#endif
