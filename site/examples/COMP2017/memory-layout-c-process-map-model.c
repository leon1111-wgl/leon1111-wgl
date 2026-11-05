// Leon | Original learning example
// Draw a process map from a table of numbers
#include <stdio.h>

/* A MODEL of one process. The addresses are chosen for teaching; a real
   system picks its own and may randomise them on every run. */
#define TEXT_START 0x00400000ul
#define TEXT_END   0x00401200ul
#define DATA_START 0x00601000ul
#define BSS_START  0x00601040ul
#define BSS_END    0x00601240ul
#define HEAP_START 0x01000000ul
#define STACK_TOP  0x7FFF0000ul

static unsigned long heap_next = HEAP_START;
static unsigned long stack_ptr = STACK_TOP;

/* The heap hands out 16-byte units, moving UP. */
static unsigned long model_malloc(unsigned long size, const char *who) {
    unsigned long block = heap_next;
    heap_next += (size + 15ul) / 16ul * 16ul;
    printf("%-9s malloc(%3lu) -> 0x%08lX, heap ends at 0x%08lX\n", who, size, block, heap_next);
    return block;
}

/* A call moves the stack pointer DOWN by the new frame's size. */
static void push_frame(const char *name, unsigned long size) {
    stack_ptr -= size;
    printf("call %-9s frame %2lu bytes, stack pointer 0x%08lX\n", name, size, stack_ptr);
}

static void pop_frame(const char *name, unsigned long size) {
    stack_ptr += size;
    printf("return %-9s stack pointer back to 0x%08lX\n", name, stack_ptr);
}

/* Each address labels the line BELOW the box above it: the lowest byte of that box. */
static void edge(unsigned long address, const char *note) {
    printf("0x%08lX  +-------------------------------+%s%s\n", address, note[0] ? " " : "", note);
}

static void box(const char *text) {
    printf("            | %-29s |\n", text);
}

int main(void) {
    unsigned long main_top = STACK_TOP;
    push_frame("main", 64);
    unsigned long read_top = stack_ptr;
    model_malloc(24, "main");
    push_frame("read_line", 48);
    unsigned long parse_top = stack_ptr;
    model_malloc(100, "read_line");
    push_frame("parse", 32);

    char line[40];
    printf("\nhigh addresses at the top, low addresses at the bottom\n");
    edge(main_top, "top of stack");
    box("main frame, 64 bytes");
    edge(read_top, "");
    box("read_line frame, 48 bytes");
    edge(parse_top, "");
    box("parse frame, 32 bytes");
    edge(stack_ptr, "<- stack pointer");
    box("v stack grows down");
    snprintf(line, sizeof line, "unused, about %lu MiB", (stack_ptr - heap_next) >> 20);
    box(line);
    box("^ heap grows up");
    edge(heap_next, "<- end of heap");
    box("heap: blocks of 32 and 112");
    edge(HEAP_START, "heap start");
    box("(unmapped)");
    edge(BSS_END, "");
    box("bss: zero-filled globals");
    edge(BSS_START, "");
    box("data: initialised globals");
    edge(DATA_START, "");
    box("(unmapped)");
    edge(TEXT_END, "");
    box("text: machine code, read-only");
    edge(TEXT_START, "lowest address");

    printf("\n");
    pop_frame("parse", 32);
    pop_frame("read_line", 48);
    printf("heap still holds %lu bytes: blocks outlive the frames that asked\n",
           heap_next - HEAP_START);
    return 0;
}
