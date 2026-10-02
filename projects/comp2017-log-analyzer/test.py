# Guoliang | Original teaching project.
"""Behavior tests: run `make test`; every generated input stays in a temp dir."""
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent
PROGRAM = ROOT / "log_analyzer"


class AnalyzerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="log-analyzer-test-")
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)

    def run_log(self, data=b"", args=None):
        if args is None:
            args = ["-"]
        self.assertTrue(PROGRAM.is_file(), "Build log_analyzer with make first")
        return subprocess.run(
            [str(PROGRAM), *args], input=data, capture_output=True,
            cwd=self.work, timeout=5, check=False,
        )

    def fields(self, result):
        lines = result.stdout.decode("ascii").splitlines()
        self.assertEqual(len(lines), 10, result.stdout)
        return dict(line.split("=", 1) for line in lines)

    def test_demo_has_hand_calculated_totals(self):
        shutil.copyfile(ROOT / "fixtures/demo.log", self.work / "demo.log")
        result = self.run_log(args=["demo.log"])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, b"")
        self.assertEqual(result.stdout, (
            b"lines=6\nvalid=6\nmalformed=0\nINFO=3\nWARN=2\nERROR=1\n"
            b"total_ms=200\nmin_ms=0\nmax_ms=100\nmean_ms=33.333\n"
        ))

    def test_mixed_file_keeps_good_rows_and_reports_exit_3(self):
        shutil.copyfile(ROOT / "fixtures/mixed.log", self.work / "mixed.log")
        result = self.run_log(args=["mixed.log"])
        self.assertEqual(result.returncode, 3)
        self.assertEqual(result.stdout, (
            b"lines=6\nvalid=3\nmalformed=3\nINFO=1\nWARN=1\nERROR=1\n"
            b"total_ms=30\nmin_ms=5\nmax_ms=15\nmean_ms=10.000\n"
        ))
        for number in (2, 4, 5):
            self.assertIn(f"line {number}: malformed record".encode(), result.stderr)

    def test_empty_has_no_invented_latency(self):
        result = self.run_log()
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, (
            b"lines=0\nvalid=0\nmalformed=0\nINFO=0\nWARN=0\nERROR=0\n"
            b"total_ms=0\nmin_ms=n/a\nmax_ms=n/a\nmean_ms=n/a\n"
        ))

    def test_duration_boundaries(self):
        result = self.run_log(b"INFO 0\nERROR 60000\n")
        self.assertEqual(result.returncode, 0)
        fields = self.fields(result)
        self.assertEqual(fields["total_ms"], "60000")
        self.assertEqual(fields["min_ms"], "0")
        self.assertEqual(fields["max_ms"], "60000")
        self.assertEqual(fields["mean_ms"], "30000.000")

    def test_integer_grammar_rejects_signs_suffixes_and_overflow(self):
        bad = [b"", b"+1", b"-1", b"1.5", b"1ms", b"1 2", b"60001",
               b"999999999999999999999999", b"0x10", b"1e2"]
        for token in bad:
            with self.subTest(token=token):
                result = self.run_log(b"INFO " + token + b"\n")
                self.assertEqual(result.returncode, 3)
                fields = self.fields(result)
                self.assertEqual(fields["valid"], "0")
                self.assertEqual(fields["malformed"], "1")
                self.assertEqual(fields["mean_ms"], "n/a")

    def test_level_must_match_whole_uppercase_word(self):
        for level in (b"info", b"DEBUG", b"INF", b"INFOx", b"WARN3"):
            with self.subTest(level=level):
                result = self.run_log(level + b" 2\n")
                self.assertEqual(result.returncode, 3)
                self.assertEqual(self.fields(result)["valid"], "0")

    def test_crlf_tabs_leading_zero_and_unterminated_last_line(self):
        result = self.run_log(b" \tINFO\t0007 \r\nWARN 3")
        self.assertEqual(result.returncode, 0)
        fields = self.fields(result)
        self.assertEqual(fields["lines"], "2")
        self.assertEqual(fields["total_ms"], "10")
        self.assertEqual(fields["mean_ms"], "5.000")

    def test_line_limit_is_exact_and_drains_one_bad_record(self):
        exact = b"INFO " + b"0" * 121 + b"1"
        too_long = b"INFO 2" + b" " * 122
        self.assertEqual(len(exact), 127)
        self.assertEqual(len(too_long), 128)
        result = self.run_log(exact + b"\n" + too_long + b"\nWARN 7\n")
        self.assertEqual(result.returncode, 3)
        fields = self.fields(result)
        self.assertEqual(fields["lines"], "3")
        self.assertEqual(fields["malformed"], "1")
        self.assertEqual(fields["valid"], "2")
        self.assertEqual(fields["total_ms"], "8")

    def test_binary_bytes_do_not_hide_suffix_or_imitate_eof(self):
        result = self.run_log(b"INFO 2\x00hidden\n\xff\nERROR 9\n")
        self.assertEqual(result.returncode, 3)
        fields = self.fields(result)
        self.assertEqual(fields["lines"], "3")
        self.assertEqual(fields["malformed"], "2")
        self.assertEqual(fields["total_ms"], "9")

    def test_blank_lines_count_and_diagnostics_are_capped(self):
        result = self.run_log(b"\n" * 20)
        self.assertEqual(result.returncode, 3)
        self.assertEqual(self.fields(result)["malformed"], "20")
        self.assertEqual(result.stderr.count(b"malformed record"), 5)
        self.assertEqual(result.stderr.count(b"further malformed lines omitted"), 1)

    def test_mean_uses_fractional_division(self):
        result = self.run_log(b"INFO 1\nINFO 2\nINFO 2\n")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(self.fields(result)["mean_ms"], "1.667")

    def test_byte_budget_accepts_exactly_one_mebibyte(self):
        row = b"INFO 0" + b" " * 121 + b"\n"
        result = self.run_log(row * 8192)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.fields(result)["valid"], "8192")
        self.assertEqual(self.fields(result)["total_ms"], "0")

    def test_byte_budget_failure_has_no_partial_report(self):
        row = b"INFO 0" + b" " * 121 + b"\n"
        result = self.run_log(row * 8192 + b"x")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, b"")
        self.assertIn(b"input exceeds 1048576 bytes", result.stderr)

    def test_argument_count_is_a_usage_error(self):
        for args in ([], ["one", "two"]):
            with self.subTest(args=args):
                result = self.run_log(args=args)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, b"")
                self.assertIn(b"usage:", result.stderr)

    def test_missing_file_is_an_io_error(self):
        result = self.run_log(args=["missing.log"])
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, b"")
        self.assertIn(b"cannot open", result.stderr)

    def test_directory_is_not_a_successful_input(self):
        result = self.run_log(args=[str(self.work)])
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, b"")
        self.assertTrue(b"cannot open" in result.stderr or
                        b"cannot read" in result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
