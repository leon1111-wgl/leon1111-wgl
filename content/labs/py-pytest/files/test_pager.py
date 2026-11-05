"""Tests for pager.py."""
import pytest

from pager import MAX_PER_PAGE, paginate


def test_first_page_defaults():
    page = paginate(95)
    assert (page.number, page.per_page, page.offset) == (1, 20, 0)
    assert page.pages == 5


def test_middle_page_offset():
    assert paginate(95, page=3, per_page=10).offset == 20


def test_per_page_is_capped():
    page = paginate(1000, page=2, per_page=500)
    assert page.per_page == MAX_PER_PAGE
    assert page.offset == MAX_PER_PAGE  # page 2 of 100-row pages skips 100 rows


def test_last_page_has_no_next():
    assert paginate(95, page=5).has_next is False


def test_page_zero_is_rejected():
    with pytest.raises(ValueError):
        paginate(10, page=0)


# Boundary cases go here.


def test_per_page_is_capped():
    assert paginate(1000, per_page=500).per_page == MAX_PER_PAGE
