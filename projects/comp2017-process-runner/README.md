# Project 2: A bounded process notebook

Leon | Original teaching project.

Mei runs a small local check before sharing her team's sensor report. She needs
three facts: what the check printed, whether she kept all of it, and how it ended.
Copying a command into a shell would hide the process and pipe rules she wants to
learn. This project builds a command-line notebook for one authorized program.

This is an original learning project, not a supplied course assignment or a
production job supervisor. Prerequisites: argument arrays, allocation ownership,
separate compilation, fork, exec/wait, and pipes.

## Build, run, and test

Use macOS or Linux with Clang, Make, and Python 3. Run from this directory:

```sh
make
./process_runner 32 -- /bin/echo 'hello team'
./process_runner 8 -- ./fixture_child burst
./process_runner 32 -- ./fixture_child fail
./process_runner 16 -- ./absent-program
make test
make clean
```

`make` uses `clang -std=c11 -Wall -Wextra -Werror -pedantic -pthread` and
`-D_POSIX_C_SOURCE=200809L`. The code is single-threaded; `-pthread` keeps the
course project build convention consistent. `make test` builds another copy in a
temporary directory and removes it afterward. It does not require `make` first.
The final two runner commands intentionally return 7 and 127, respectively.
Run the commands individually if your terminal script stops on a nonzero status.

The interface is `process_runner CAP -- PROGRAM [ARG ...]`. CAP is decimal digits
from 0 through 65536. A name without `/` is searched using inherited PATH. Prefer
an explicit path when choosing a specific executable. Shell quotes in the
examples make one argument before the runner starts; the runner passes the
existing argument vector to `execvp`. It does not join arguments, expand `$HOME`,
expand `*`, split spaces, or interpret `;`.

For the first command, standard output is exactly:

```text
stdout="hello team\n"
captured_bytes=11
truncated=no
child_exit=0
```

For the burst command, the fixture writes 1,048,576 `A` bytes and the report is:

```text
stdout="AAAAAAAA"
captured_bytes=8
truncated=yes
child_exit=0
```

For the failing check, standard output is:

```text
stdout="check failed\n"
captured_bytes=13
truncated=no
child_exit=7
```

For the missing program, standard output is:

```text
stdout=""
captured_bytes=0
truncated=no
child_exit=127
```

It also writes `process_runner: execvp failed` followed by a newline to stderr.
The failure did not strand the child: the parent reached EOF and reaped it.

## Five connected milestones

1. **Specify the notebook.** Read `main.c` and `process.h`. Validate the cap before
   allocating or forking. Borrow `&argv[3]` without building a command string.
   The caller owns the allocated buffer; the process module only writes into it.
2. **Give the child a channel.** Read `execute_child` in `process.c`. `pipe` creates
   a read end and a write end. After `fork`, each process has descriptors for both.
   The child closes its read end, duplicates its write end onto stdout (fd 1),
   closes the original write descriptor, then calls `execvp`.
3. **Keep memory bounded without blocking progress.** Read `drain_output`.
   Each read may return any positive number up to 4096. Save only what fits,
   but read again even when the capture is full. CAP=0 discards everything while
   still letting the child finish. The final `tail` fixture needs no newline.
4. **Finish the lifecycle.** Read `process_run` and `report`. The parent closes
   its write end immediately. It drains until EOF, closes its read end, and calls
   `waitpid` for this child. Decode status with `WIFEXITED`/`WEXITSTATUS` or
   `WIFSIGNALED`/`WTERMSIG`, never by guessing bits in the raw status integer.
5. **Prove the boundaries.** Read `fixtures/child.c` and `test.py`. Use literal
   expected byte counts, return codes, stdout, and stderr. Try a cap of 3, 4, and
   0 for a four-byte fragment. Then test a much larger burst and a missing program.
   These are concept checks for this project, not answers to another assignment.

## Descriptor ownership and ordering

| Resource | Owner after setup | Release |
| --- | --- | --- |
| `channel[0]`, read descriptor | Parent | Close after EOF or read failure; child closes its copy before exec |
| `channel[1]`, original write descriptor | Neither after setup | Parent closes immediately; child closes after `dup2` |
| Child stdout, descriptor 1 | Executed child | Child closes it or process termination closes it |
| Capture buffer | `main` in parent | `free` on process failure or after the report |
| Direct child PID/status | Parent | `waitpid(child, ..., 0)` consumes its termination status |
| Argument strings | C runtime/caller | Borrowed, never freed or rewritten by this module |

An empty pipe gives EOF only after **all** write descriptors referring to it have
closed. Closing the parent's copy is essential. A grandchild could keep stdout
open, delaying EOF even after the direct child exits. EOF and child termination
are separate events: a child could close stdout and keep running. Waiting after
the drain is therefore still necessary. A successful wait tells us the direct
child terminated; it does not wait for its descendants.

There is no chosen scheduling order between parent and child. A successful read
returns bytes already written into the pipe. The final report happens after the
drain and successful wait. If the parent waited first, a full pipe could block the
child's write, while the parent waits for that same child to finish. Keeping only
a small prefix does not justify stopping the drain.

For N output bytes and cap C, stored bytes = min(N, C), truncation = (N > C).
The algorithm reads O(N) bytes and uses O(C + 4096) memory. It deliberately does
not count all discarded bytes, avoiding an unbounded total-byte counter. The
report can contain up to four characters per stored byte because of escaping.

## Output, errors, and boundaries

- Only stdout is captured. Stdin and stderr are inherited. Diagnostics go directly
  to the existing stderr sink; their timing relative to the later stdout report
  is not specified. Captured bytes are displayed as printable ASCII with `\n`,
  `\r`, `\t`, `\\`, `\"`, and two-digit `\xHH` escapes. NUL and high bytes are
  supported. This is a byte view, not decoded Unicode or a raw binary copy.
- Normal child exit codes are returned unchanged. Signal termination is printed
  as `child_signal=N` and mapped to `128+N` on the supported systems. The report
  distinguishes a signal from an ordinary child exit of the same numeric code.
- Usage errors return 2. Runner allocation/setup/read/wait/report errors return
  125 when handled. Child redirection failure uses `_exit(126)`; exec failure
  writes a fixed diagnostic and uses `_exit(127)`. A program can itself return
  126 or 127; there is no separate exec-error pipe to disambiguate them. A runner
  error has no complete child report. OS error wording from `perror` can vary.
- `read`, `waitpid`, child diagnostic `write`, and `dup2` retry `EINTR`. On a read
  failure the parent sends SIGKILL to its own direct child, closes the read end,
  and still attempts to reap it. A failed `fork` closes both descriptors while
  preserving errno. The small child path uses `_exit`, so it does not flush a
  copied parent stdio buffer or call inherited `atexit` handlers.
- The API assumes a single-threaded caller, open standard descriptors, ordinary
  blocking I/O, no competing child reaper, and default SIGCHLD handling. It checks
  descriptors 0, 1, and 2 before creating the pipe so pipe descriptors exceed 2.
  Cleanup closes are best effort and are not retried; portable recovery from
  interrupted `close` across every POSIX variant is outside this example.
- This is not a sandbox. The program inherits the current directory, environment,
  stdin, stderr, and other non-close-on-exec descriptors. POSIX `execvp` can invoke
  a command interpreter for an executable text file with an unrecognized format.
  This fallback interprets the selected file; the runner still never constructs
  a shell command from its arguments. Use the supplied compiled fixture or an
  executable you are authorized to run.
- There is no deadline, process-tree cleanup, resource quota, or signal-forwarding
  policy. A child waiting for input, a descendant holding the pipe open, a blocked
  stderr sink, or a child that never exits can stall the runner. Interrupting the
  runner may leave a child alive; no application signal handlers are installed.
  A broken report pipe can terminate it by default SIGPIPE. Adding cancellation
  correctly requires a wider design than one extra `kill` call.

The tests launch only the finite fixture helper, `/bin/echo`, and one deliberately
missing path. Each runner gets an isolated process group and an 8-second test
watchdog; timeout cleanup targets that test group. The fixture creates no
children, reads no input, and writes at most 1 MiB. A 30-second build timeout
bounds compilation. Fourteen tests cover malformed caps, spaces and metacharacters,
empty output, exact/over limits, binary escaping, stderr, normal/nonzero/signal
status, and exec failure. They do not force rare allocation/fork/read failures,
EINTR delivery, every schedule, or process-tree cancellation.

## Primary references

- [POSIX fork](https://pubs.opengroup.org/onlinepubs/9799919799/functions/fork.html)
- [POSIX exec family](https://pubs.opengroup.org/onlinepubs/9799919799/functions/exec.html)
- [POSIX pipe](https://pubs.opengroup.org/onlinepubs/9799919799/functions/pipe.html)
- [POSIX read](https://pubs.opengroup.org/onlinepubs/9799919799/functions/read.html)
- [POSIX wait and waitpid](https://pubs.opengroup.org/onlinepubs/9699919799/functions/wait.html)
- [POSIX dup2](https://pubs.opengroup.org/onlinepubs/9799919799/functions/dup.html)
- [POSIX _exit](https://pubs.opengroup.org/onlinepubs/9799919799/functions/_exit.html)
