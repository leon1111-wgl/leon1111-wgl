"""Nightly sales report.  Usage: python3 report.py ROWS"""
import sys
import time
from collections import Counter, defaultdict

from cleaning import prepare
from data import make_orders


def money(cents):
    return f"{cents / 100:,.2f}"


def summarise(rows):
    by_region = defaultdict(int)
    by_customer = Counter()
    for row in rows:
        by_region[row["region"]] += row["amount_cents"]
        by_customer[row["customer"]] += row["amount_cents"]
    return by_region, by_customer


def run(n):
    """Build the report for n exported rows. Returns (report lines, stage timings)."""
    t0 = time.perf_counter()
    raw = make_orders(n)
    t1 = time.perf_counter()
    rows = prepare(raw)
    t2 = time.perf_counter()
    by_region, by_customer = summarise(rows)
    t3 = time.perf_counter()

    lines = [
        f"orders exported: {len(raw)}",
        f"orders kept: {len(rows)} ({len(raw) - len(rows)} duplicates dropped)",
        "revenue by region:",
    ]
    for region in sorted(by_region):
        lines.append(f"  {region:<6} {money(by_region[region]):>14}")
    lines.append("top customers:")
    for customer, cents in by_customer.most_common(3):
        lines.append(f"  {customer:<10} {money(cents):>12}")
    timings = {"load": t1 - t0, "clean": t2 - t1, "summarise": t3 - t2}
    return lines, timings


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    lines, timings = run(n)
    print("\n".join(lines))
    stages = "  ".join(f"{name} {seconds:.2f}s" for name, seconds in timings.items())
    print(f"timing: {stages}", file=sys.stderr)


if __name__ == "__main__":
    main()
