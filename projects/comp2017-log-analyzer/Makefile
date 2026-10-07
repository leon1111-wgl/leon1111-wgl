# Leon | Original teaching project.
CC = clang
CFLAGS = -std=c11 -Wall -Wextra -Werror -pedantic -pthread
OBJECTS = main.o reader.o record.o stats.o

.PHONY: all test clean
all: log_analyzer

log_analyzer: $(OBJECTS)
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $(OBJECTS) $(LDLIBS)

main.o: main.c reader.h record.h stats.h
reader.o: reader.c reader.h
record.o: record.c record.h
stats.o: stats.c stats.h record.h reader.h

%.o: %.c
	$(CC) $(CPPFLAGS) $(CFLAGS) -c $< -o $@

test: log_analyzer
	python3 test.py

clean:
	rm -f log_analyzer $(OBJECTS)
