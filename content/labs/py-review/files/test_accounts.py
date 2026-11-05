"""What accounts_to_lock should do, written from the docstring and the incident notes."""
import logging

import pytest

from accounts import accounts_to_lock


def batch(*events):
    return [f"2026-03-02T09:{minute % 60:02d}:00Z,{user},{outcome}" for minute, (user, outcome) in enumerate(events)]


def fails(user, times):
    return [(user, "FAIL")] * times


def test_account_at_the_threshold_is_reported():
    lines = batch(*fails("leon", 3), ("mia", "OK"))
    assert accounts_to_lock(lines) == ["leon"]


def test_account_below_the_threshold_is_not_reported():
    lines = batch(*fails("mia", 2), ("mia", "OK"))
    assert accounts_to_lock(lines) == []


def test_batches_do_not_share_state():
    assert accounts_to_lock(batch(*fails("leon", 3))) == ["leon"]
    assert accounts_to_lock(batch(*fails("emma", 3))) == ["emma"]


def test_accounts_already_locked_are_not_reported_again():
    lines = batch(*fails("leon", 3), *fails("jack", 3))
    assert accounts_to_lock(lines, locked=["leon"]) == ["jack"]


def test_the_callers_list_is_left_alone():
    already = ["leon"]
    accounts_to_lock(batch(*fails("jack", 3)), locked=already)
    assert already == ["leon"]


def test_one_damaged_line_is_logged_not_hidden(caplog):
    lines = batch(*fails("noah", 3), *[("ok-user", "OK")] * 400)
    lines[1] = "2026-03-02T09:01:00Z,noah"  # cut off mid-line
    with caplog.at_level(logging.WARNING, logger="lockout"):
        accounts_to_lock(lines)
    assert "line 2" in caplog.text


def test_a_mostly_unreadable_batch_is_refused():
    with pytest.raises(ValueError):
        accounts_to_lock(["not a log line"] * 10)
