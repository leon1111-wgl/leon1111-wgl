// Leon | Original learning example
// Read bytes until the operation reports the end
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    FILE *stream = tmpfile();
    if (stream == NULL)
        return 1;
    const unsigned char bytes[] = {'A', 0, 'B'};
    if (fwrite(bytes, 1, sizeof bytes, stream) != sizeof bytes) {
        fclose(stream);
        return 1;
    }
    if (fseek(stream, 0, SEEK_SET) != 0) {
        fclose(stream);
        return 1;
    }
    size_t count = 0;
    int ch;
    while ((ch = fgetc(stream)) != EOF) {
        printf("byte %zu=%d\n", count, ch);
        count++;
    }
    if (ferror(stream)) {
        fclose(stream);
        return 1;
    }
    printf("count=%zu ended=%s\n", count, feof(stream) ? "yes" : "no");
    return fclose(stream) == 0 ? 0 : 1;
}
