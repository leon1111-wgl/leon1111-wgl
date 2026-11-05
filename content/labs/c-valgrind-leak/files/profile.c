#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "profile.h"

static char *dup_string(const char *s)
{
    size_t n = strlen(s) + 1;
    char *p = malloc(n);
    if (p != NULL) {
        memcpy(p, s, n);
    }
    return p;
}

void profile_free(struct profile *p)
{
    if (p == NULL) {
        return;
    }
    free(p->name);
    free(p->host);
    free(p);
}

struct profile *profile_parse(const char *spec)
{
    char name[32], host[64];
    long port;

    struct profile *p = calloc(1, sizeof *p);
    if (p == NULL) {
        return NULL;
    }
    if (sscanf(spec, "%31s %63s %ld", name, host, &port) != 3) {
        free(p);
        return NULL;
    }
    p->name = dup_string(name);
    p->host = dup_string(host);
    if (p->name == NULL || p->host == NULL) {
        free(p->name);
        free(p->host);
        free(p);
        return NULL;
    }
    if (port < 1 || port > 65535) {
        free(p);
        return NULL;
    }
    p->port = (unsigned)port;
    return p;
}
