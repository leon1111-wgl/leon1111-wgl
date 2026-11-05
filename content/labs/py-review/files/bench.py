"""Time accounts_to_lock on 3,000 and 12,000 log lines and print how the cost grew."""
import time

from accounts import accounts_to_lock


def make_lines(count):
    """count lines: every user fails exactly three times, so each one is reported."""
    return [f"2026-03-02T09:00:00Z,user{i // 3},FAIL" for i in range(count)]


def best(count):
    lines = make_lines(count)
    times = []
    for _ in range(2):
        start = time.perf_counter()
        reported = accounts_to_lock(lines, locked=[])
        times.append(time.perf_counter() - start)
    return min(times), len(reported)


small, large = 3000, 12000
t_small, n_small = best(small)
t_large, n_large = best(large)
print(f"{'lines':>7} {'seconds':>8} {'accounts reported':>18}")
print(f"{small:>7} {t_small:>8.3f} {n_small:>18}")
print(f"{large:>7} {t_large:>8.3f} {n_large:>18}")
print(f"growth: lines x{large // small}, time x{t_large / t_small:.0f}")
