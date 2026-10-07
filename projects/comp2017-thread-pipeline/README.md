# Project 3 · A bounded file-statistics pipeline

Leon | Original teaching project. [中文说明](README.zh.md)

Mina helps a school robotics club archive its daily notes. She receives a list of small text files and wants a count of their bytes, lines, and words. Some notes are empty. One ends without a newline. A missing file must remain visible in the report while the other notes are still counted. She wants to try several workers, but the report must always follow her original file list.

Her first useful tool counts one file precisely. She then places numbered jobs into a four-slot queue. Workers take those numbers and open their own files. The queue applies backpressure: when all four slots are occupied, Mina's producer waits instead of allocating another slot. A worker's completion time never determines its output position. Main prints the numbered results only after all workers have finished.

This is an original guided engineering project, not a supplied assignment solution. C11, POSIX threads, Clang, Make, and Python 3 are required. The source targets macOS and Linux; no network or third-party Python packages are used.

## Build and run

From this project directory:

```sh
make
./thread_pipeline 3 fixtures/morning.txt fixtures/evening.txt fixtures/empty.txt
```

Program stdout (the compiler commands printed by `make` are separate):

```text
job=1 bytes=37 lines=2 words=6
job=2 bytes=26 lines=2 words=5
job=3 bytes=0 lines=0 words=0
summary files=3 ok=3 failed=0
```

An empty file list is valid. Workers wake when main closes the empty queue:

```sh
./thread_pipeline 16
```

```text
summary files=0 ok=0 failed=0
```

A missing file does not discard completed work:

```sh
./thread_pipeline 2 fixtures/morning.txt fixtures/missing.txt fixtures/evening.txt
```

```text
job=1 bytes=37 lines=2 words=6
job=2 error=open
job=3 bytes=26 lines=2 words=5
summary files=3 ok=2 failed=1
```

The first two runs exit with 0. The missing-file run exits with 1 and also writes a diagnostic to stderr. Its operating-system error wording may vary. Job 2 means the second file argument, not worker 2. Files may repeat; each argument is a separate job.

```sh
./thread_pipeline 0 fixtures/morning.txt
```

This prints usage to stderr, prints no stdout, and exits with 2. WORKERS must contain only decimal digits and represent 1 through 16; leading zeros are accepted. At most 128 file arguments are accepted. There is no option parser: every argument after WORKERS is a file path.

## Decide what is being counted

* Bytes count every byte read, including whitespace and zero bytes. This is not a Unicode character count.
* Lines count LF bytes (`\n`) plus one when a nonempty file ends with a different byte. Thus empty is 0 lines, `a` is 1, `a\n` is 1, and `\n\n` is 2. A final newline does not invent another empty line. This differs from tools that count only newline characters.
* Words are maximal runs separated by exactly space, tab, LF, CR, vertical tab, or form feed. The definition is independent of locale. Zero bytes and non-ASCII bytes are ordinary non-separators, not string terminators or decoded letters.
* Each regular file may contain at most 8,388,608 bytes (8 MiB). A larger file produces `error=too-large`; its partial counters are not presented as a complete answer. `in_word` survives each 4096-byte read, so a word crossing a buffer boundary stays one word.

The synthetic fixtures are 37-byte morning notes, 26-byte evening notes without a final LF, two blank lines, a zero-byte file, and six whitespace bytes. The whitespace fixture has two logical lines because bytes follow its LF. These definitions are the contract against which tests compare the program.

## Read the implementation in five stages

1. **Specify a file result.** Read `stats.h`, then `separator` and `count_stream` in `stats.c`. Track `bytes`, `lines`, `words`, `in_word`, and `last` on `a b\n`. The loop counts word beginnings. EOF finishes the final logical line exactly once. `read` returns a signed count; check for an error before converting it to `size_t`.
2. **Build the bounded queue.** Read `queue.h` and `queue_push`. `head` identifies the next occupied slot. The next insertion is `(head + count) % 4`. The invariant is `0 <= count <= 4`. A push waits while full and open. A pop waits while empty and open. Every check and every mutation uses the same mutex. `pthread_cond_wait` releases that mutex while waiting and reacquires it before returning. A notification asks a waiter to check again; it does not reserve a slot. Use `while`, including after a spurious wakeup.
3. **Give workers exclusive results.** Read `WorkerContext` and `consume` in `main.c`. Main gives each input one index exactly once. A pop removes that index while holding the queue lock, so only one worker receives it. The worker owns `results[index]` during scanning and opens/closes its own descriptor. File reads happen outside the queue lock. This lets other workers take jobs while a scan is running.
4. **Close, drain, and join.** Read `queue_close` and the final half of `main`. Closing forbids future pushes but does not remove queued work. A pop returns false only when the queue is empty and closed. Broadcasting wakes every idle consumer, including all sixteen consumers for zero jobs. Main joins each successfully created worker before printing or destroying shared objects.
5. **Validate ordinary and failed runs.** Read `parse_workers`, startup cleanup, `print_results`, and `test.py`. No jobs are published until every requested worker exists. If thread creation fails, close the still-empty queue, join only the workers actually created, destroy the queue, and return failure. A file error occupies its own result slot while other jobs continue. Stable output is tested against independent expected values, never against worker timing.

## Ownership and execution phases

```text
main: initialize queue + context + result storage
      |
      +--> create all workers --> publish indices --> close queue
                 |                    |                  |
workers:         +--> wait/pop -------+--> scan --> pop --+--> drain --> return
      |
main: join every created worker --> destroy queue --> print slots 0..J-1

creation failure: close empty queue --> join created workers --> destroy --> exit 1
```

The queue, context, and result array live in main's stack frame until after all joins. `argv` paths live throughout the process and are borrowed without mutation. Queue entries own no file or allocation; they are indices. A worker owns its local read buffer and opened file descriptor. `scan_file` attempts to close that descriptor on every post-open path. Main owns all joinable thread handles and joins only successful creations.

Initialization before `pthread_create` makes the initialized context available to workers. The mutex orders queue reads and writes and safely hands an index from producer to consumer. Distinct array elements are distinct objects: workers never write the same `FileStats`. Main does not read any result until successful `pthread_join` calls have synchronized it with every worker's completion. These ownership and phase rules remove the need for a result mutex. Merely promising that main will “probably run later” would not be sufficient.

## Errors and deliberate limits

`scan_file` reports open, metadata, non-regular-file, read, size-limit, and close errors. The first failure is preserved. Interrupted reads (`EINTR`) retry; ordinary short reads are processed and followed by another read. Nonblocking open avoids waiting for a FIFO writer before rejecting non-regular inputs with `fstat`. This is intended for the supplied regular fixtures and other stable regular files, not arbitrary devices, hostile paths, live-changing files, or a secure filesystem sandbox.

Queue initialization returns a checked error and unwinds initialized components. Thread creation has orderly cleanup. Unexpected runtime mutex/condition/join/destroy errors instead use a documented fail-fast policy: print an error and terminate the process, without promising graceful cleanup or a complete report. These pthread functions return their error code directly. The program does not use `errno` to interpret them. An unsuccessful `close` is reported without retrying an uncertain descriptor state.

There is no cancellation, signal-driven shutdown, or per-file wall-clock deadline. A slow filesystem may still delay a regular-file read, and repeated signals may repeatedly interrupt it. Tests have subprocess timeouts; the program itself does not guarantee a time bound. Input files must remain unchanged for reproducible counts. Native Windows is outside this POSIX target. Checked stdout failures return failure; a broken pipe can also terminate the process through the usual SIGPIPE behavior.

Counting costs O(B + J), where B is the bytes scanned and J is the job count. Queue operations use constant storage and constant work apart from waiting. The queue has four indices; result storage has a fixed upper bound of 128 entries; there are at most 16 workers, each with one 4096-byte read buffer plus its runtime thread stack. Storage does not grow with file length. A byte-limit check can read one extra buffer before rejecting an oversized file. Tiny fixtures provide correctness evidence, not evidence of a speedup. Storage contention and thread startup can make extra workers slower.

## Test and investigate

```sh
make test
python3 test.py --tsan
make clean
```

`make test` builds and runs in a temporary copy, even if the source directory already contains a local build. It never changes source fixtures. Every subprocess has a timeout. The optional second command requires a working Clang ThreadSanitizer compiler and runtime; an unavailable or failing sanitizer run is an error, not a silent pass.

The test suite checks exact fixture output, no jobs, empty files, one and sixteen workers, below/above queue capacity, maximum job count, malformed worker counts, missing files, directory/FIFO rejection, buffer-boundary words, binary bytes, and both sides of the file-size limit. A separate queue probe checks FIFO order, close-and-drain, and push-after-close rejection. Forty-eight repeated runs scan 37 bounded synthetic files with 1, 2, 4, and 16 workers. All compare with an independent byte/regular-expression oracle and one-worker output.

Temporary test-only C shims inject thread creation failure before the first worker and after two workers, a read failure, and one interrupted read. They exercise cleanup without exhausting system resources. These compile-time substitutions are not switches in the shipped program. Stress tests and ThreadSanitizer can expose bugs; neither proves that every possible schedule is correct. The invariant and happens-before argument remain necessary.

If a zero-job run hangs, inspect the close broadcast and the `count == 0 && !closed` predicate. If a final unterminated line disappears, inspect the EOF correction. If output changes order, look for worker-side printing or a missing join. If words split at a 4096-byte boundary, check whether `in_word` was incorrectly reset inside the read loop. If a missing file appears as zero counts, inspect whether the status is tested before printing counters.

## File map and next experiments

`main.c` owns CLI validation, pool startup, publication, joins, and output. `queue.h` declares the bounded state; `queue.c` implements its locked transitions. `stats.h` defines result/error data; `stats.c` scans one regular file. `Makefile` supplies strict build/test/clean targets. `test.py` provides the independent oracle, stress checks, and fault injection. Both README files explain the same project in different languages. The five files in `fixtures/` are synthetic inputs with intentionally different boundaries.

For a first extension, make queue capacity configurable with a bounded range, then test capacities 1, 4, and 8 against unchanged result output. For a second, add measured performance experiments on fixed, larger local fixtures. Record total bytes, compiler options, worker count, elapsed time, repeated runs, and filesystem-cache conditions; compute throughput as bytes divided by seconds. Accept a speed claim only when measurements support it. Keep timing outside deterministic result output.

## Primary references

The design explanations are original. These official POSIX pages support the API contracts:

* [Condition waits and predicate rechecking](https://pubs.opengroup.org/onlinepubs/9799919799/functions/pthread_cond_clockwait.html)
* [pthread_join](https://pubs.opengroup.org/onlinepubs/9799919799.2024edition/functions/pthread_join.html)
* [Memory synchronization, section 4.15.2](https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap04.html)
* [pthread_create, Issue 6 API contract](https://pubs.opengroup.org/onlinepubs/000095399/functions/pthread_create.html)
* [read](https://pubs.opengroup.org/onlinepubs/9799919799/functions/read.html)
