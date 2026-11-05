"""Lock-out check: which accounts failed to sign in too often in one auth-log batch."""
import logging

log = logging.getLogger("lockout")


def parse_line(line):
    """One log line looks like: 2026-03-02T09:14:07Z,leon,FAIL"""
    stamp, user, outcome = line.strip().split(",")
    return stamp, user, outcome


def accounts_to_lock(lines, threshold=3, locked=[]):
    """Return accounts with at least `threshold` failed sign-ins in this batch.

    Accounts already in `locked` are not reported again.
    """
    failures = []
    for line in lines:
        try:
            stamp, user, outcome = parse_line(line)
        except Exception:
            continue
        if outcome == "FAIL":
            failures.append(user)

    for user in failures:
        if failures.count(user) >= threshold and user not in locked:
            log.info("locking %s", user)
            locked.append(user)
    return locked
