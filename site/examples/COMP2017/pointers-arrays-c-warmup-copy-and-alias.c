// Leon | Original learning example
// Start here: a copy and an address
#include <stdio.h>
#include <stdlib.h>
static void change_copy(int value) {
    value = 9;
    printf("inside copy=%d\n", value);
}
static void change_object(int *address) {
    *address = 9;
}
int main(void) {
    int original = 4;
    int copy = original;
    int *alias = &original;
    change_copy(original);
    printf("after value call: original=%d copy=%d\n", original, copy);
    change_object(alias);
    printf("after address call: original=%d copy=%d\n", original, copy);
    return 0;
}
