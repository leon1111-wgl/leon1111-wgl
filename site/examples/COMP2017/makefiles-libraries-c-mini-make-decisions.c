// Leon | Original learning example
// Model what make decides to rebuild
#include <stdio.h>
#include <string.h>

/* A tiny model of what make decides. Time is a counter: a bigger number is a newer file. */
#define MAX_FILES 8
#define MAX_PREREQS 3

struct File {
    const char *name;
    int mtime;  /* 0 means the file does not exist */
};

struct Rule {
    const char *target;
    const char *prereqs[MAX_PREREQS + 1];  /* ends with NULL */
    const char *recipe;
};

static struct File files[MAX_FILES] = {
    {"main.c", 1}, {"util.c", 2}, {"util.h", 3}, {"main.o", 0}, {"util.o", 0}, {"app", 0}};
static int file_count = 6;
static int clock_now = 3;

static const struct Rule rules[] = {
    {"app", {"main.o", "util.o", NULL}, "$(CC) $^ -o $@"},
    {"main.o", {"main.c", "util.h", NULL}, "$(CC) $(CFLAGS) -c $< -o $@"},
    {"util.o", {"util.c", "util.h", NULL}, "$(CC) $(CFLAGS) -c $< -o $@"},
};

static struct File *find_file(const char *name) {
    for (int i = 0; i < file_count; i++)
        if (strcmp(files[i].name, name) == 0)
            return &files[i];
    return NULL;
}

static const struct Rule *find_rule(const char *target) {
    for (size_t i = 0; i < sizeof rules / sizeof rules[0]; i++)
        if (strcmp(rules[i].target, target) == 0)
            return &rules[i];
    return NULL;
}

/* Replace $@, $<, $^, $(CC) and $(CFLAGS) in a recipe template. */
static void expand(const struct Rule *rule, char *out, size_t size) {
    size_t used = 0;
    for (const char *p = rule->recipe; *p != '\0' && used + 1 < size;) {
        char piece[80] = "";
        size_t length = 1;
        if (strncmp(p, "$@", 2) == 0) {
            snprintf(piece, sizeof piece, "%s", rule->target);
            length = 2;
        } else if (strncmp(p, "$<", 2) == 0) {
            snprintf(piece, sizeof piece, "%s", rule->prereqs[0]);
            length = 2;
        } else if (strncmp(p, "$^", 2) == 0) {
            for (int i = 0; rule->prereqs[i] != NULL; i++)
                snprintf(piece + strlen(piece), sizeof piece - strlen(piece), "%s%s", i ? " " : "", rule->prereqs[i]);
            length = 2;
        } else if (strncmp(p, "$(CC)", 5) == 0) {
            snprintf(piece, sizeof piece, "clang");
            length = 5;
        } else if (strncmp(p, "$(CFLAGS)", 9) == 0) {
            snprintf(piece, sizeof piece, "-std=c11 -Wall -Wextra -Werror -pedantic");
            length = 9;
        } else {
            piece[0] = *p;
            piece[1] = '\0';
        }
        for (const char *q = piece; *q != '\0' && used + 1 < size; q++)
            out[used++] = *q;
        p += length;
    }
    out[used] = '\0';
}

/* Returns 1 if the target was rebuilt. Prerequisites are brought up to date first. */
static int build(const char *target) {
    const struct Rule *rule = find_rule(target);
    struct File *file = find_file(target);
    if (rule == NULL)
        return 0;  /* a source file: nothing to run */
    int rebuilt = 0, newest = 0;
    for (int i = 0; rule->prereqs[i] != NULL; i++) {
        rebuilt |= build(rule->prereqs[i]);
        int t = find_file(rule->prereqs[i])->mtime;
        if (t > newest)
            newest = t;
    }
    if (file->mtime == 0 || newest > file->mtime) {
        char command[160];
        expand(rule, command, sizeof command);
        printf("  %s\n", command);
        file->mtime = ++clock_now;
        return 1;
    }
    return rebuilt;
}

static void run_make(const char *title) {
    printf("%s\n", title);
    if (!build("app"))
        printf("  make: 'app' is up to date.\n");
}

static void touch(const char *name) {
    find_file(name)->mtime = ++clock_now;
}

int main(void) {
    printf("Makefile\n");
    for (size_t i = 0; i < sizeof rules / sizeof rules[0]; i++) {
        printf("%s:", rules[i].target);
        for (int j = 0; rules[i].prereqs[j] != NULL; j++)
            printf(" %s", rules[i].prereqs[j]);
        printf("\n\t%s\n", rules[i].recipe);
    }
    printf("\n");

    run_make("$ make   (fresh checkout)");
    run_make("$ make   (again, nothing changed)");
    touch("util.c");
    run_make("$ make   (after editing util.c)");
    touch("util.h");
    run_make("$ make   (after editing util.h)");
    return 0;
}
