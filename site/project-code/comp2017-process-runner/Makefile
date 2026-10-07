# Leon | Original teaching project.
CC = clang
CFLAGS = -std=c11 -Wall -Wextra -Werror -pedantic -pthread
CPPFLAGS = -D_POSIX_C_SOURCE=200809L

.PHONY: all test clean
all: process_runner fixture_child

process_runner: main.c process.c process.h
	$(CC) $(CPPFLAGS) $(CFLAGS) main.c process.c -o $@

fixture_child: fixtures/child.c
	$(CC) $(CPPFLAGS) $(CFLAGS) fixtures/child.c -o $@

test:
	python3 test.py

clean:
	rm -f process_runner fixture_child
