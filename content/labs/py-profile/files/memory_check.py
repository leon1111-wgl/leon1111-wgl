"""Peak extra memory of two ways to drop duplicate order ids (20,000 rows)."""
import tracemalloc

from data import make_orders


def with_list(rows):
    kept, seen = [], []
    for row in rows:
        if row["order_id"] in seen:
            continue
        seen.append(row["order_id"])
        kept.append(row)
    return kept


def with_set(rows):
    kept, seen = [], set()
    for row in rows:
        if row["order_id"] in seen:
            continue
        seen.add(row["order_id"])
        kept.append(row)
    return kept


def peak_kib(work, *args):
    tracemalloc.start()
    result = work(*args)
    peak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    return peak / 1024, result


rows_peak, rows = peak_kib(make_orders, 20000)
list_peak, a = peak_kib(with_list, rows)
set_peak, b = peak_kib(with_set, rows)
assert a == b, "both variants must keep the same rows"

print(f"{'what':<34} {'peak KiB':>9}")
print(f"{'building the 20,000 input rows':<34} {rows_peak:>9.0f}")
print(f"{'de-duplicate with a list':<34} {list_peak:>9.0f}")
print(f"{'de-duplicate with a set':<34} {set_peak:>9.0f}")
