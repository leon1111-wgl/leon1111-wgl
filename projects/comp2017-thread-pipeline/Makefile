# Leon | Original teaching project.
CC = clang
CPPFLAGS = -D_POSIX_C_SOURCE=200809L
CFLAGS = -std=c11 -Wall -Wextra -Werror -pedantic -O2 -pthread
LDFLAGS = -pthread

.PHONY: all test clean
all: thread_pipeline

thread_pipeline: main.o queue.o stats.o
	$(CC) $(LDFLAGS) -o $@ main.o queue.o stats.o

main.o: main.c queue.h stats.h
queue.o: queue.c queue.h
stats.o: stats.c stats.h

test:
	python3 test.py

clean:
	rm -f thread_pipeline main.o queue.o stats.o
