#include <stdio.h>
#include <string.h>
#include "profile.h"

static int check(const char *label, int ok)
{
    printf("%-30s %s\n", label, ok ? "ok" : "FAIL");
    return ok ? 0 : 1;
}

int main(void)
{
    int failed = 0;

    struct profile *p = profile_parse("staging 10.0.0.5 8443");
    failed += check("valid spec parses", p != NULL && p->port == 8443
                    && strcmp(p->name, "staging") == 0 && strcmp(p->host, "10.0.0.5") == 0);
    profile_free(p);

    failed += check("port 99999 is rejected", profile_parse("staging 10.0.0.5 99999") == NULL);
    failed += check("missing port is rejected", profile_parse("staging 10.0.0.5") == NULL);
    failed += check("port 0 is rejected", profile_parse("edge 10.0.0.9 0") == NULL);

    return failed ? 1 : 0;
}
