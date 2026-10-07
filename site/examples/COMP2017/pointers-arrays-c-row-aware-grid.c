// Leon | Original learning example
// Use the actual row type
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int grid[2][3] = {{2, 4, 6}, {8, 10, 12}};
    int (*row)[3] = grid;
    for (size_t r = 0; r < 2; r++) {
        int total = 0;
        for (size_t c = 0; c < 3; c++)
            total += row[r][c];
        printf("row %zu sum=%d\n", r, total);
    }
    printf("second row last=%d\n", (*(row + 1))[2]);
    printf("row elements=%zu\n", sizeof *row / sizeof(*row)[0]);
    return 0;
}
