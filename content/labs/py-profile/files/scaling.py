"""Run the report at two sizes and print how the cost grew."""
import time

from report import run


def measure(n, repeats):
    """Best of `repeats` runs, as (total seconds, clean-stage seconds)."""
    best = None
    for _ in range(repeats):
        start = time.perf_counter()
        _, timings = run(n)
        total = time.perf_counter() - start
        if best is None or total < best[0]:
            best = (total, timings["clean"])
    return best


small_n, large_n = 2000, 20000
small = measure(small_n, repeats=3)
large = measure(large_n, repeats=1)

print(f"{'rows':>8} {'total_s':>9} {'clean_s':>9}")
print(f"{small_n:>8} {small[0]:>9.3f} {small[1]:>9.3f}")
print(f"{large_n:>8} {large[0]:>9.3f} {large[1]:>9.3f}")
print(f"growth: rows x{large_n // small_n}, total time x{large[0] / small[0]:.0f}, clean stage x{large[1] / small[1]:.0f}")
