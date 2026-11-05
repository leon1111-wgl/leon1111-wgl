// Leon | Original learning example
// Resolve names against an archive and a shared library
#include <stdio.h>
#include <string.h>

/* A model of how a linker resolves names. Sizes are made up for the story. */
#define MAX_NAMES 4
#define MAX_SYMBOLS 8

struct Unit {  /* an object file, or one member of an archive */
    const char *name;
    const char *defines[MAX_NAMES];  /* each list ends with NULL */
    const char *needs[MAX_NAMES];
    int bytes;
    int pulled;
};

static struct Unit main_o = {"main.o", {"main", NULL}, {"area_circle", NULL}, 1200, 0};
static struct Unit library[3];  /* libgeo members, in archive order */

struct Link {
    const char *undefined[MAX_SYMBOLS];
    int undefined_count;
    const char *defined[MAX_SYMBOLS];
    int defined_count;
    int bytes;
};

static int has(const char *const list[], int count, const char *name) {
    for (int i = 0; i < count; i++)
        if (strcmp(list[i], name) == 0)
            return i;
    return -1;
}

static void take(struct Link *link, struct Unit *unit) {
    unit->pulled = 1;
    link->bytes += unit->bytes;
    for (int i = 0; unit->defines[i] != NULL; i++) {
        link->defined[link->defined_count++] = unit->defines[i];
        int at = has(link->undefined, link->undefined_count, unit->defines[i]);
        if (at >= 0)
            link->undefined[at] = link->undefined[--link->undefined_count];
    }
    for (int i = 0; unit->needs[i] != NULL; i++)
        if (has(link->defined, link->defined_count, unit->needs[i]) < 0 &&
            has(link->undefined, link->undefined_count, unit->needs[i]) < 0)
            link->undefined[link->undefined_count++] = unit->needs[i];
    printf("  take %s\n", unit->name);
}

static int wanted(const struct Link *link, const struct Unit *unit) {
    for (int i = 0; unit->defines[i] != NULL; i++)
        if (has(link->undefined, link->undefined_count, unit->defines[i]) >= 0)
            return 1;
    return 0;
}

/* A static archive: keep scanning it until no member is newly needed. */
static void scan_archive(struct Link *link) {
    for (int pass = 1, changed = 1; changed; pass++) {
        changed = 0;
        for (int i = 0; i < 3; i++)
            if (!library[i].pulled && wanted(link, &library[i])) {
                if (!changed)
                    printf("  pass %d over libgeo.a\n", pass);
                take(link, &library[i]);
                changed = 1;
            }
    }
}

/* A shared library: names are matched now, but no code is copied. */
static void use_shared(struct Link *link) {
    for (int i = 0; i < 3; i++)
        for (int j = 0; library[i].defines[j] != NULL; j++) {
            int at = has(link->undefined, link->undefined_count, library[i].defines[j]);
            if (at >= 0) {
                printf("  libgeo.so provides %s: only a dependency is recorded\n", library[i].defines[j]);
                link->undefined[at] = link->undefined[--link->undefined_count];
            }
        }
}

static void finish(const struct Link *link) {
    for (int i = 0; i < link->undefined_count; i++)
        printf("  error: undefined reference to '%s'\n", link->undefined[i]);
    if (link->undefined_count == 0)
        printf("  ok: the executable holds %d bytes of code\n", link->bytes);
}

static void reset_units(void) {
    static const struct Unit fresh[3] = {
        {"square.o", {"square", NULL}, {NULL}, 400, 0},
        {"area.o", {"area_circle", "area_rect", NULL}, {"square", NULL}, 900, 0},
        {"perim.o", {"perim_rect", NULL}, {NULL}, 700, 0}};
    memcpy(library, fresh, sizeof fresh);
    main_o.pulled = 0;
}

int main(void) {
    printf("build the library\n");
    printf("  clang -c -fPIC square.c area.c perim.c\n");
    printf("  ar rcs libgeo.a square.o area.o perim.o\n");
    printf("  clang -shared -o libgeo.so square.o area.o perim.o\n\n");

    struct Link link;

    printf("clang main.o libgeo.a -o app_static\n");
    reset_units();
    memset(&link, 0, sizeof link);
    take(&link, &main_o);
    scan_archive(&link);
    for (int i = 0; i < 3; i++)
        if (!library[i].pulled)
            printf("  left out %s\n", library[i].name);
    finish(&link);

    printf("\nclang libgeo.a main.o -o app_wrong_order\n");
    reset_units();
    memset(&link, 0, sizeof link);
    scan_archive(&link);
    printf("  nothing is missing yet, so no member is taken\n");
    take(&link, &main_o);
    finish(&link);

    printf("\nclang main.o -L. -lgeo -o app_shared\n");
    reset_units();
    memset(&link, 0, sizeof link);
    take(&link, &main_o);
    use_shared(&link);
    finish(&link);
    printf("  libgeo.so (2000 bytes) is loaded when the program starts and shared by every user\n");
    return 0;
}
