#!/usr/bin/env python3
# Leon | Original teaching project.
"""Build only in a temporary copy; use independent byte oracles and timeouts."""
import argparse
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

SOURCE = Path(__file__).resolve().parent
FLAGS = ["-D_POSIX_C_SOURCE=200809L", "-std=c11", "-Wall", "-Wextra",
         "-Werror", "-pedantic", "-O2", "-pthread"]
LIMIT = 8 * 1024 * 1024


def command(args, cwd, timeout=20):
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True,
                          timeout=timeout, check=False)


def successful(args, cwd, timeout=30):
    result = command(args, cwd, timeout)
    assert result.returncode == 0, (args, result.stdout, result.stderr)
    return result


def expected_line(index, data):
    # A regular expression oracle, independent of the C in_word state machine.
    lines = data.count(b"\n") + int(bool(data) and not data.endswith(b"\n"))
    words = len(re.findall(rb"[^ \t\r\n\v\f]+", data))
    return f"job={index} bytes={len(data)} lines={lines} words={words}\n"


def expect_files(root, files, workers, binary="thread_pipeline"):
    result = successful([f"./{binary}", str(workers), *files], root)
    expected = "".join(expected_line(i, (root / path).read_bytes())
                       for i, path in enumerate(files, 1))
    expected += f"summary files={len(files)} ok={len(files)} failed=0\n"
    assert result.stdout == expected, (result.stdout, expected)
    assert result.stderr == "", result.stderr
    return result.stdout


def variant(root, name, source, define, shim, flags):
    # Only a temporary translation unit is instrumented; shipped C is unchanged.
    (root / f"{name}_shim.c").write_text(shim, encoding="utf-8")
    successful(["clang", *flags, f"-D{define}", "-c", source,
                "-o", f"{name}.o"], root)
    successful(["clang", *flags, "-c", f"{name}_shim.c", "-o",
                f"{name}_shim.o"], root)
    objects = [f"{name}.o" if item == source else item.replace(".c", ".o")
               for item in ("main.c", "queue.c", "stats.c")]
    successful(["clang", *flags, *objects, f"{name}_shim.o", "-o", name], root)


def run_tests(root, flags):
    successful(["make", "all", "CFLAGS=" + " ".join(flags),
                "LDFLAGS=" + " ".join(flags)], root)
    supplied = [f"fixtures/{name}.txt" for name in
                ("morning", "evening", "blank", "empty", "spaces")]
    expect_files(root, [], 16)
    expect_files(root, supplied[:1], 1)
    expect_files(root, supplied[:2], 16)
    expect_files(root, supplied, 4)
    print("PASS empty queue, empty file, and fewer/more jobs than capacity")

    # Hard-coded expected counts catch an error shared by both implementations.
    exact = successful(["./thread_pipeline", "3", *supplied], root)
    assert exact.stdout == (
        "job=1 bytes=37 lines=2 words=6\n"
        "job=2 bytes=26 lines=2 words=5\n"
        "job=3 bytes=2 lines=2 words=0\n"
        "job=4 bytes=0 lines=0 words=0\n"
        "job=5 bytes=6 lines=2 words=0\n"
        "summary files=5 ok=5 failed=0\n")
    print("PASS exact fixture counts including final unterminated line")

    binary_bytes = b"x" * 4095 + b"YZ\x00\xff \r\n\tfinal"
    (root / "boundary.bin").write_bytes(binary_bytes)
    expect_files(root, ["boundary.bin"], 2)
    print("PASS word crossing read-buffer boundary and non-ASCII bytes")

    for args in ([], ["0"], ["17"], ["-1"], ["+2"], ["2x"], [""],
                 [" 2"], ["99999999999999999999999999"],
                 ["1", *([supplied[0]] * 129)]):
        result = command(["./thread_pipeline", *args], root)
        assert result.returncode == 2 and result.stdout == "", result
        assert result.stderr.startswith("usage: thread_pipeline WORKERS"), result
    expect_files(root, supplied[:1], "0002")
    expect_files(root, [supplied[0]] * 128, 16)
    print("PASS malformed CLI, accepted leading zeros, and 128-job boundary")

    result = command(["./thread_pipeline", "4", supplied[0], "missing.txt",
                      supplied[1]], root)
    assert result.returncode == 1, result
    assert result.stdout == (expected_line(1, (root / supplied[0]).read_bytes()) +
                             "job=2 error=open\n" +
                             expected_line(3, (root / supplied[1]).read_bytes()) +
                             "summary files=3 ok=2 failed=1\n"), result.stdout
    assert "job 2 (missing.txt): open:" in result.stderr, result.stderr
    print("PASS missing file preserves other results and returns failure")

    os.mkfifo(root / "pipe")
    result = command(["./thread_pipeline", "2", "fixtures", "pipe"], root)
    assert result.returncode == 1, result
    assert result.stdout == ("job=1 error=not-regular\n"
                             "job=2 error=not-regular\n"
                             "summary files=2 ok=0 failed=2\n"), result.stdout
    print("PASS directory and FIFO rejected without waiting for a writer")

    (root / "limit.txt").write_bytes(b"z" * LIMIT)
    expect_files(root, ["limit.txt"], 1)
    with (root / "limit.txt").open("ab") as handle:
        handle.write(b"z")
    result = command(["./thread_pipeline", "1", "limit.txt"], root)
    assert result.returncode == 1, result
    assert result.stdout == ("job=1 error=too-large\n"
                             "summary files=1 ok=0 failed=1\n"), result.stdout
    print("PASS exact byte limit and oversized input without partial statistics")

    stress = []
    for i in range(37):
        path = f"stress-{i:02}.txt"
        data = (b"alpha\tbeta\n\n" * (i * 71)) + (b"tail" if i % 2 else b"")
        (root / path).write_bytes(data)
        stress.append(path)
    reference = expect_files(root, stress, 1)
    for repeat in range(12):
        for workers in (1, 2, 4, 16):
            output = expect_files(root, stress, workers)
            assert output == reference, (repeat, workers)
    print("PASS 48 repeated schedules: 37 jobs, workers 1/2/4/16, stable output")

    probe = r'''/* Leon | Original teaching project. */
#include "queue.h"
#include <assert.h>
int main(void) {
    WorkQueue queue;
    assert(queue_init(&queue) == 0);
    for (size_t i = 0; i < QUEUE_CAPACITY; i++) {
        assert(queue_push(&queue, i + 10));
    }
    queue_close(&queue);
    assert(!queue_push(&queue, 99));
    for (size_t i = 0; i < QUEUE_CAPACITY; i++) {
        size_t job;
        assert(queue_pop(&queue, &job));
        assert(job == i + 10);
    }
    size_t job;
    assert(!queue_pop(&queue, &job));
    queue_close(&queue);
    queue_destroy(&queue);
    return 0;
}
'''
    (root / "queue_probe.c").write_text(probe, encoding="utf-8")
    successful(["clang", *flags, "queue_probe.c", "queue.o", "-o", "queue_probe"], root)
    successful(["./queue_probe"], root)
    print("PASS queue close drains FIFO entries and rejects new work")

    for after in (0, 2):
        shim = r'''/* Leon | Original teaching project. */
#include <errno.h>
#include <pthread.h>
static unsigned int calls;
int fixture_create(pthread_t *thread, const pthread_attr_t *attributes,
                   void *(*start)(void *), void *argument) {
    if (calls++ == FAIL_AFTER) {
        return EAGAIN;
    }
    return pthread_create(thread, attributes, start, argument);
}
'''.replace("FAIL_AFTER", str(after))
        name = f"create_failure_{after}"
        variant(root, name, "main.c", "pthread_create=fixture_create", shim, flags)
        result = command([f"./{name}", "4", *supplied], root)
        assert result.returncode == 1 and result.stdout == "", result
        assert f"thread creation failed after {after} workers" in result.stderr, result
    print("PASS injected creation failure before first/after two workers; no hang")

    for mode in ("error", "interrupt"):
        body = "errno = EIO; return -1;" if mode == "error" else (
            "static int first = 1; if (first) { first = 0; errno = EINTR; return -1; }"
            " return read(descriptor, buffer, count);")
        shim = r'''/* Leon | Original teaching project. */
#include <errno.h>
#include <stddef.h>
#include <unistd.h>
ssize_t fixture_read(int descriptor, void *buffer, size_t count) {
    (void)descriptor; (void)buffer; (void)count;
    BODY
}
'''.replace("BODY", body)
        name = f"read_{mode}"
        variant(root, name, "stats.c", "read=fixture_read", shim, flags)
        if mode == "error":
            result = command([f"./{name}", "1", supplied[0]], root)
            assert result.returncode == 1, result
            assert result.stdout == ("job=1 error=read\n"
                                     "summary files=1 ok=0 failed=1\n"), result.stdout
            assert "read:" in result.stderr, result.stderr
        else:
            expect_files(root, supplied[:1], 1, name)
    print("PASS injected read error and interrupted-read retry")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tsan", action="store_true",
                        help="require a working clang ThreadSanitizer runtime")
    args = parser.parse_args()
    flags = FLAGS + (["-O1", "-g", "-fsanitize=thread"] if args.tsan else [])
    with tempfile.TemporaryDirectory(prefix="guoliang-thread-test-") as directory:
        root = Path(directory) / "project"
        shutil.copytree(SOURCE, root, ignore=shutil.ignore_patterns(
            "*.o", "thread_pipeline", "__pycache__"))
        run_tests(root, flags)
    print("All pipeline tests passed" + (" (ThreadSanitizer)." if args.tsan else "."))


if __name__ == "__main__":
    main()
