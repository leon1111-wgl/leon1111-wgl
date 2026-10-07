#!/usr/bin/env python3
# Leon | Original teaching project.
"""Build a temporary copy and exercise only bounded, local fixture programs."""
import os
from pathlib import Path
import shutil
import signal
import subprocess
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parent


class RunnerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix="guoliang-process-test-")
        cls.addClassCleanup(cls.temp.cleanup)
        cls.work = Path(cls.temp.name)
        for name in ("main.c", "process.c", "process.h", "Makefile"):
            shutil.copy2(SOURCE / name, cls.work / name)
        shutil.copytree(SOURCE / "fixtures", cls.work / "fixtures")
        built = subprocess.run(["make", "all"], cwd=cls.work, text=True,
                               capture_output=True, timeout=30, check=False)
        if built.returncode:
            raise AssertionError(built.stdout + built.stderr)

    def run_runner(self, *args):
        # A new group lets a timeout clean up both runner and its own child.
        child = subprocess.Popen(["./process_runner", *args], cwd=self.work,
                                 stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, start_new_session=True)
        try:
            out, err = child.communicate(timeout=8)
        except subprocess.TimeoutExpired:
            os.killpg(child.pid, signal.SIGKILL)
            child.communicate()
            self.fail("bounded fixture timed out; possible pipe/wait deadlock")
        return child.returncode, out.decode("ascii"), err.decode("ascii")

    def test_echo_and_literal_space_argument(self):
        # Catches splitting one argument or losing the trailing newline.
        self.assertEqual(self.run_runner("32", "--", "/bin/echo", "hello team"),
                         (0, 'stdout="hello team\\n"\ncaptured_bytes=11\n'
                          'truncated=no\nchild_exit=0\n', ""))

    def test_metacharacters_are_arguments(self):
        # No shell may expand the dollar sign, wildcard, or semicolon.
        self.assertEqual(self.run_runner("64", "--", "./fixture_child", "args",
                                        "two words", "$HOME;*"),
                         (0, 'stdout="[two words][$HOME;*]"\ncaptured_bytes=20\n'
                          'truncated=no\nchild_exit=0\n', ""))

    def test_large_output_is_drained_after_cap(self):
        self.assertEqual(self.run_runner("8", "--", "./fixture_child", "burst"),
                         (0, 'stdout="AAAAAAAA"\ncaptured_bytes=8\n'
                          'truncated=yes\nchild_exit=0\n', ""))

    def test_zero_cap_still_drains(self):
        self.assertEqual(self.run_runner("0", "--", "./fixture_child", "burst"),
                         (0, 'stdout=""\ncaptured_bytes=0\n'
                          'truncated=yes\nchild_exit=0\n', ""))

    def test_empty_output_is_not_truncation(self):
        self.assertEqual(self.run_runner("0", "--", "./fixture_child", "empty"),
                         (0, 'stdout=""\ncaptured_bytes=0\n'
                          'truncated=no\nchild_exit=0\n', ""))

    def test_exact_cap_and_final_fragment(self):
        self.assertEqual(self.run_runner("4", "--", "./fixture_child", "fragment"),
                         (0, 'stdout="tail"\ncaptured_bytes=4\n'
                          'truncated=no\nchild_exit=0\n', ""))

    def test_one_byte_over_cap(self):
        self.assertEqual(self.run_runner("3", "--", "./fixture_child", "fragment"),
                         (0, 'stdout="tai"\ncaptured_bytes=3\n'
                          'truncated=yes\nchild_exit=0\n', ""))

    def test_nonzero_child_status_is_returned(self):
        self.assertEqual(self.run_runner("32", "--", "./fixture_child", "fail"),
                         (7, 'stdout="check failed\\n"\ncaptured_bytes=13\n'
                          'truncated=no\nchild_exit=7\n', ""))

    def test_missing_program_is_reaped(self):
        self.assertEqual(self.run_runner("16", "--", "./absent-program"),
                         (127, 'stdout=""\ncaptured_bytes=0\n'
                          'truncated=no\nchild_exit=127\n',
                          "process_runner: execvp failed\n"))

    def test_stderr_is_inherited_not_captured(self):
        self.assertEqual(self.run_runner("16", "--", "./fixture_child", "stderr"),
                         (0, 'stdout="ok\\n"\ncaptured_bytes=3\n'
                          'truncated=no\nchild_exit=0\n', "diagnostic\n"))

    def test_byte_escaping_is_lossless_for_the_prefix(self):
        self.assertEqual(self.run_runner("16", "--", "./fixture_child", "bytes"),
                         (0, 'stdout="\\x00\\xFF\\\"\\\\\\t\\r\\n"\ncaptured_bytes=7\n'
                          'truncated=no\nchild_exit=0\n', ""))

    def test_signal_status_is_reported(self):
        code, out, err = self.run_runner("16", "--", "./fixture_child", "signal")
        self.assertEqual(code, 128 + signal.SIGTERM)
        self.assertEqual(out, 'stdout=""\ncaptured_bytes=0\ntruncated=no\n'
                             f'child_signal={signal.SIGTERM}\n')
        self.assertEqual(err, "")

    def test_maximum_cap(self):
        code, out, err = self.run_runner("65536", "--", "./fixture_child", "burst")
        self.assertEqual(code, 0)
        self.assertEqual(out, 'stdout="' + "A" * 65536 + '"\ncaptured_bytes=65536\n'
                             'truncated=yes\nchild_exit=0\n')
        self.assertEqual(err, "")

    def test_bad_cli_never_starts_a_child(self):
        cases = [(), ("8", "--"), ("8", "--", ""),
                 ("-1", "--", "./fixture_child", "empty"),
                 ("65537", "--", "./fixture_child", "empty"),
                 ("8x", "--", "./fixture_child", "empty"),
                 (" 8", "--", "./fixture_child", "empty"),
                 ("9999999999999999999999999", "--", "./fixture_child", "empty"),
                 ("8", "wrong", "./fixture_child", "empty")]
        for args in cases:
            with self.subTest(args=args):
                code, out, err = self.run_runner(*args)
                self.assertEqual(code, 2)
                self.assertEqual(out, "")
                self.assertEqual(err, "usage: process_runner CAP -- PROGRAM [ARG ...]\n"
                                     "CAP must be decimal digits from 0 to 65536.\n")


if __name__ == "__main__":
    unittest.main(verbosity=2)
