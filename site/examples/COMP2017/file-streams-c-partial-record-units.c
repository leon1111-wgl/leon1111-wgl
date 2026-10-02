// Guoliang | Original learning example
// Count bytes and complete records separately
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    FILE *stream = tmpfile();
    if (stream == NULL)
        return 1;
    const unsigned char bytes[] = {1, 2, 3, 4, 5, 6, 7};
    if (fwrite(bytes, 1, sizeof bytes, stream) != sizeof bytes) {
        fclose(stream);
        return 1;
    }
    if (fseek(stream, 0, SEEK_SET) != 0) {
        fclose(stream);
        return 1;
    }
    unsigned char record[12] = {0};
    size_t records = fread(record, sizeof record, 1, stream);
    if (ferror(stream)) {
        fclose(stream);
        return 1;
    }
    printf("complete records=%zu\n", records);
    if (fseek(stream, 0, SEEK_SET) != 0) {
        fclose(stream);
        return 1;
    }
    size_t received = fread(record, 1, sizeof record, stream);
    if (ferror(stream)) {
        fclose(stream);
        return 1;
    }
    printf("received bytes=%zu\n", received);
    puts(received == sizeof record ? "record accepted" : "truncated record rejected");
    return fclose(stream) == 0 ? 0 : 1;
}
