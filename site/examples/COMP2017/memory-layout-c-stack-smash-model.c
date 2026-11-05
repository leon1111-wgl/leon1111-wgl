// Leon | Original learning example
// Model a stack smash safely and stop it
#include <stdio.h>
#include <string.h>

/* A MODEL of neighbouring bytes in one stack frame. A real compiler picks
   the order of locals itself; the point here is only that they are adjacent. */
struct Frame {
    char name[8];         /* a local buffer */
    unsigned canary;      /* a guard value stored right after it */
    unsigned return_tag;  /* stands in for the saved return address */
};

#define CANARY     0xC0FFEE00u
#define RETURN_TAG 0xA1B2C3D4u

static void reset(struct Frame *f) {
    memset(f, 0, sizeof *f);
    f->canary = CANARY;
    f->return_tag = RETURN_TAG;
}

/* Like strcpy: copies the text and its zero byte, never asking how big name is.
   It goes through the whole frame's own bytes so this demo stays well defined;
   in real code the same mistake is undefined behaviour. */
static void unchecked_copy(struct Frame *f, const char *text) {
    size_t n = strlen(text) + 1;
    if (n > sizeof *f)
        n = sizeof *f;
    memcpy(f, text, n);
}

/* Refuse text that does not fit, leaving room for the zero byte. */
static int checked_copy(struct Frame *f, const char *text) {
    size_t n = strlen(text);
    if (n >= sizeof f->name)
        return -1;
    memcpy(f->name, text, n + 1);
    return 0;
}

int main(void) {
    const char *inputs[] = {"Mia", "NoahIrisJack", "NoahIrisJackLeo"};
    struct Frame frame;
    printf("model frame: name[%zu], then canary, then return tag\n", sizeof frame.name);

    for (int i = 0; i < 3; i++) {
        reset(&frame);
        unchecked_copy(&frame, inputs[i]);
        printf("unchecked %-16s name=\"%.8s\" canary %s, return tag %s\n", inputs[i], frame.name,
               frame.canary == CANARY ? "intact" : "OVERWRITTEN",
               frame.return_tag == RETURN_TAG ? "intact" : "OVERWRITTEN");
        if (frame.canary != CANARY)
            printf("  guard check fails: stack smashing detected, abort before return\n");
    }

    for (int i = 0; i < 3; i++) {
        reset(&frame);
        int status = checked_copy(&frame, inputs[i]);
        printf("checked   %-16s %s, canary %s\n", inputs[i],
               status == 0 ? "stored" : "rejected as too long",
               frame.canary == CANARY ? "intact" : "OVERWRITTEN");
    }
    return 0;
}
