"""Show what accounts_to_lock does in two everyday situations.

Run this after you have written your own review comments, not before.
"""
import logging

from accounts import accounts_to_lock

logging.basicConfig(level=logging.WARNING, format="log: %(levelname)s %(message)s")


def batch(*events):
    return [f"2026-03-02T09:{minute:02d}:00Z,{user},{outcome}" for minute, (user, outcome) in enumerate(events)]


print("1. two unrelated batches, one after the other")
first = batch(("leon", "FAIL"), ("leon", "FAIL"), ("leon", "FAIL"), ("mia", "OK"))
second = batch(("emma", "FAIL"), ("emma", "FAIL"), ("emma", "FAIL"), ("jack", "OK"))
print("   batch 1 ->", accounts_to_lock(first))
print("   batch 2 ->", accounts_to_lock(second))

print("2. iris fails three times, but the third line was cut off when the log rotated")
damaged = batch(("iris", "FAIL"), ("iris", "FAIL")) + ["2026-03-02T09:02:00Z,iris"]
print("   result  ->", accounts_to_lock(damaged, locked=[]))
print("   (any warning from the logger would appear above as a line starting 'log:')")
