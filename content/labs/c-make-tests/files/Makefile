# Makefile v0: the shell script build.sh, translated one-to-one.
BUILD     = build
SANITIZE  =
CFLAGS    =
LDFLAGS   = $(SANITIZE)

OBJS      = $(BUILD)/main.o $(BUILD)/ring.o $(BUILD)/stats.o $(BUILD)/util.o
TEST_OBJS = $(BUILD)/test_ring.o $(BUILD)/ring.o $(BUILD)/stats.o $(BUILD)/util.o

all: $(BUILD)/sampler $(BUILD)/test_ring

$(BUILD)/sampler: $(OBJS)
	$(CC) $(LDFLAGS) -o $@ $(OBJS)

$(BUILD)/test_ring: $(TEST_OBJS)
	$(CC) $(LDFLAGS) -o $@ $(TEST_OBJS)

$(BUILD)/%.o: %.c
	@mkdir -p $(BUILD)
	$(CC) $(CFLAGS) -c -o $@ $<

clean:
	rm -rf build build-asan

.PHONY: all test asan clean
