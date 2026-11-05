#ifndef UTIL_H
#define UTIL_H

/* A 32-bit hash of a label such as "node-eu-west-1-0042", used to pick a shard. */
unsigned hash_label(const char *s);

#endif
