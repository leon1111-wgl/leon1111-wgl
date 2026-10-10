// Leon | Original learning example
// Define a file format instead of dumping a struct
#include <assert.h>
#include <limits.h>
#include <stdint.h>
#include <stdio.h>
#if CHAR_BIT != 8
#error This teaching format requires eight-bit bytes
#endif
static void encode(uint16_t value, unsigned char out[4]) {
    out[0] = 0x4c; out[1] = 1;
    out[2] = (unsigned char)(value >> 8);
    out[3] = (unsigned char)(value & 0xffu);
}
static int decode(const unsigned char *in, size_t size, uint16_t *value) {
    if (size != 4 || in[0] != 0x4c || in[1] != 1) return 0;
    uint16_t result = (uint16_t)(((unsigned)in[2] << 8) | in[3]);
    *value = result;
    return 1;
}
int main(void) {
    unsigned char wire[4]; encode(513, wire);
    printf("wire: %u %u %u %u\n", (unsigned)wire[0], (unsigned)wire[1],
           (unsigned)wire[2], (unsigned)wire[3]);
    FILE *file = tmpfile();
    if (file == NULL) return 1;
    if (fwrite(wire, 1, sizeof wire, file) != sizeof wire ||
        fseek(file, 0, SEEK_SET) != 0) { fclose(file); return 1; }
    unsigned char readback[5];
    size_t count = fread(readback, 1, sizeof readback, file);
    int failed = ferror(file);
    int closed = fclose(file);
    if (failed || closed != 0) return 1;
    uint16_t value = 999;
    int valid = decode(readback, count, &value);
    assert(valid && value == 513);
    printf("decoded: %u\n", (unsigned)value);
    wire[1] = 2;
    int wrong_version = decode(wire, 4, &value);
    int incomplete = decode(wire, 3, &value);
    assert(!wrong_version && !incomplete && value == 513);
    puts("bad version and short record rejected; output unchanged");
    return 0;
}
