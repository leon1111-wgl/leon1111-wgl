#ifndef PROFILE_H
#define PROFILE_H

/* A connection profile parsed from "NAME HOST PORT", for example
 * "staging 10.0.0.5 8443". The profile owns name and host. */
struct profile {
    char *name;
    char *host;
    unsigned port;
};

/* Returns a new profile, or NULL if the spec is malformed or the port is
 * outside 1..65535. The caller releases a non-NULL result with profile_free. */
struct profile *profile_parse(const char *spec);

/* Releases a profile and everything it owns. NULL is allowed. */
void profile_free(struct profile *p);

#endif
