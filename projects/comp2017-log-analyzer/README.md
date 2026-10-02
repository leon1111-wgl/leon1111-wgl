# Streaming log analyzer

Guoliang | Original teaching project for COMP2017. [中文版](README.zh.md).

Guoliang is testing a small classroom robot simulator. After each simulated action,
it writes a severity and a duration, such as `WARN 40`. Reading the whole trace by
eye makes it easy to miss a slow action. Guoliang wants a tool that counts each
severity and summarizes durations. Some records are broken, so the report must
also say how much data was rejected. All fixtures are invented teaching data.
This is an original engineering project, not a supplied course assignment.

## Build, run, test

You need Clang, make, and Python 3 on macOS or Linux. From the repository root:

```sh
cd projects/comp2017-log-analyzer
make
./log_analyzer fixtures/demo.log
make test
```

For a downloaded project folder, open a terminal in that folder and start with
`make`. The Makefile compiles four C files separately and links them. Its default
flags are `-std=c11 -Wall -Wextra -Werror -pedantic -pthread`; this project creates
no threads. `make clean` removes only the executable and its object files.

To analyze standard input, use `-` as the only argument:

```sh
printf 'INFO 12\n' | ./log_analyzer -
```

The tool prints ten `key=value` lines. `total_ms` is the sum of valid durations;
`mean_ms = total_ms / valid`, rounded for display to three decimal places. The
minimum and maximum also use only valid rows. Empty data has `n/a` latency values:
no observation is different from an observation with a duration of zero.

## Agree on the input before writing the loop

A record is an uppercase `INFO`, `WARN`, or `ERROR`, then one or more spaces or
tabs, then decimal digits representing **0 through 60000 milliseconds**. Leading
and trailing spaces/tabs and leading zeroes are allowed. Signs, fractions, units,
extra columns, comments, and unknown levels are rejected. A blank line is one
malformed record. `ERROR` is a valid severity; it is not a parser error.

LF ends a physical line. A final CR is removed, which accepts CRLF files and a
final CR before EOF. The last record does not need LF. At most **127 bytes before
LF**, including a final CR, are allowed. An embedded NUL or longer line rejects
the entire physical line. The reader consumes its remaining bytes so they cannot
be mistaken for another row. The whole input may contain at most **1,048,576
bytes**, including line endings. One extra byte may be read to detect excess.

| Exit | Meaning | stdout |
|---|---|---|
| 0 | Input completed; every record was valid, or input was empty | Complete summary |
| 3 | Input completed; at least one record was malformed | Summary of valid rows plus rejected count |
| 2 | Wrong number of arguments | Empty |
| 1 | Open/read/close failure, byte budget exceeded, or reported output failure | No report for input failures; an output failure may leave a prefix |

Warnings go to stderr, with physical line numbers for the first five bad rows.
One further message says later warnings were omitted; all bad rows are still
counted. Run `echo $?` immediately after a command to see its exit status.

## Five learning milestones

1. **Follow one row through a working program.** Run the `INFO 12` command above.
   Find `main`, `parse_record`, `stats_accept`, and `stats_print`. The text becomes
   a `struct record`, then changes a `struct stats`, then becomes output text.
   Draw those four boxes before reading error branches. The checkpoint is
   `valid=1`, `INFO=1`, `total_ms=12`, and `mean_ms=12.000`.
2. **Make a parser promise.** Read `record.h` before `record.c`. A successful call
   assigns the caller's record; failure leaves it unchanged. The local
   `candidate` makes that promise possible. Trace `INFO 60000`, then `INFO 60001`.
   Before computing `value * 10 + digit`, the code checks
   `value <= (60000 - digit) / 10`. This both enforces the range and avoids an
   overflowing intermediate. Confirm that `INFO 12ms` is rejected even though
   its beginning looks numeric. The checkpoint is clean separation between
   valid severity `ERROR` and malformed text.
3. **Read a stream without losing line boundaries.** Read `reader.h`, then
   `reader.c`. The buffer needs 128 bytes: 127 data bytes plus `\0`. Keep `fgetc`'s
   return value in an `int` so EOF remains distinguishable from a byte. A bad
   line is drained before the next call. Test 127 bytes, 128 bytes, and a valid
   row after the oversized row. The checkpoint is exactly one rejection, with
   the later valid record intact. The reader borrows `FILE *`; it never closes it.
4. **Accumulate a useful report.** Read `stats.h` and `stats.c`. Initialize the
   struct with `{0}`. For the first accepted value, set both extrema from that
   value; initializing minimum to zero alone would give wrong results for
   positive durations. Use `uint64_t` for counts and sums, `unsigned` for a
   bounded duration, and `double` only when computing the mean. Recalculate the
   demo by hand: sum 200, count 6, min 0, max 100. The checkpoint is the exact
   demo output below and the empty-input `n/a` output.
5. **Finish the command-line contract and prove it.** Revisit `main.c`. Mark every
   path from `fopen` to `fclose`. A file opened here is closed here; borrowed stdin
   is left to the runtime. Input errors suppress a misleading partial report.
   Run `make test`, then read a test that deliberately rejects input. It must
   inspect the exit code, report, and diagnostics. The checkpoint is all 16
   tests passing, including the 1 MiB limit and the mixed-data exit status 3.

The website provides longer bilingual steps and extracts from these same final
files. Extracts are reading aids, not standalone programs. Build the full project.
These checkpoints are original concept checks, not answers to supplied exercises.

## File reading order

| File | Why it exists |
|---|---|
| `record.h`, `record.c` | Record shape and complete text-validation contract |
| `reader.h`, `reader.c` | Byte budget, line framing, and stream errors |
| `stats.h`, `stats.c` | State invariants, aggregates, and report formatting |
| `main.c` | Arguments, resource ownership, pipeline, and exit policy |
| `Makefile` | Rebuild the needed translation units and link once |
| `fixtures/demo.log` | Six valid rows with hand-calculable results |
| `fixtures/mixed.log` | Three valid and three invalid rows |
| `fixtures/empty.log` | Zero bytes, not one blank line |
| `test.py` | Sixteen tests against the executable using temporary directories |

Headers are interfaces: read their promises first. Source files implement those
promises. No parser or statistics function stores a pointer to the line buffer;
it is safe to reuse the buffer on the next iteration. The main function owns the
statistics for its whole run. No application heap allocation is required.

## Three actual runs

These stdout blocks were captured from the compiled program. Build once with
`make` before running them. stderr is described separately.

### Valid robot trace

```sh
./log_analyzer fixtures/demo.log
```

```text
lines=6
valid=6
malformed=0
INFO=3
WARN=2
ERROR=1
total_ms=200
min_ms=0
max_ms=100
mean_ms=33.333
```

Exit 0; stderr is empty. `ERROR=1` counts a simulated event, not a program failure.

### A trace with damaged records

```sh
./log_analyzer fixtures/mixed.log
```

```text
lines=6
valid=3
malformed=3
INFO=1
WARN=1
ERROR=1
total_ms=30
min_ms=5
max_ms=15
mean_ms=10.000
```

Exit 3. stderr warns about lines 2, 4, and 5: unknown `DEBUG`, negative `-1`, and
out-of-range `60001`. Their durations never reach the aggregates.

### No observations

```sh
./log_analyzer fixtures/empty.log
```

```text
lines=0
valid=0
malformed=0
INFO=0
WARN=0
ERROR=0
total_ms=0
min_ms=n/a
max_ms=n/a
mean_ms=n/a
```

Exit 0; stderr is empty. An empty file has no malformed record.

## Debug with a prediction

If mean `1.667` becomes `1.000` for durations 1, 2, 2, inspect the division's types:
converting after integer division is too late. If a valid row after a long row is
lost or counted twice, inspect draining at the reader boundary. If all positive
inputs report minimum zero, inspect first-record initialization. If a file appears
successful after a read failure, inspect `ferror`, not just `EOF`. Start with the
smallest input that demonstrates the problem, and keep it as a regression test.

Tests cover valid/mixed/empty input; numeric and severity grammar; 0 and 60000;
CRLF, tabs, leading zeroes, and missing final LF; 127/128-byte rows; NUL and 0xff;
warning suppression; fractional mean; exact/excessive byte budgets; usage; missing
files; and directories. Expected totals are literal, hand-checked values, not a
second copy of the C algorithm. Every invocation has a five-second test timeout.
Generated files live only in each test's temporary directory and are removed.
The suite does not simulate every filesystem, output, or close failure.

## Decisions, limits, and next steps

Memory used by our state is O(1); time is O(B) for B bytes consumed. Standard I/O
also maintains its own implementation-managed buffers. The byte cap limits work
and proves the total fits: at most 1,048,576 accepted records times 60,000 ms is
62,914,560,000, safely below the `uint64_t` maximum. The actual accepted-record
limit is smaller because records use multiple bytes. Changing limits requires
reviewing that proof; a static assertion checks its multiplication bound.

We choose a small explicit grammar and a fixed buffer to make contracts visible.
This is not a parser for arbitrary real-world logs. There are no timestamps,
percentiles, live file following, or per-level latency summaries. A byte limit is
not a wall-clock deadline: stdin may wait for its producer. Use completed files
for the first project. A broken output pipe may trigger the normal POSIX SIGPIPE
signal rather than our exit 1 path. File read/write/close errors returned by the C
library are checked; failures writing diagnostic stderr are not retried.

To extend the project, add per-level duration sums and means. Acceptance: the demo
must give INFO 30/3 = 10.000, WARN 70/2 = 35.000, ERROR 100/1 = 100.000, and an absent
level must print `n/a`. Alternatively add a `--strict` mode. Acceptance: the first
bad row stops processing with exit 3 and no stdout, while default mode remains
unchanged. Write the new behavior tests before changing the implementation.

## Primary references

- [WG14 N1570: C11 committee draft](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf): sections 7.20, 7.21.7.1, and 7.21.10 explain integer types, `fgetc`, and stream status.
- [Clang user manual](https://clang.llvm.org/docs/UsersManual.html): language and diagnostic options.
- [Python subprocess documentation](https://docs.python.org/3/library/subprocess.html): argument lists, captured output, return codes, and timeouts.
