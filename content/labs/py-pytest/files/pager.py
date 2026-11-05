"""Pagination arithmetic for the order list endpoint."""
from dataclasses import dataclass
from math import ceil

MAX_PER_PAGE = 100


@dataclass(frozen=True)
class Page:
    number: int      # 1-based, as in the URL
    per_page: int    # after the cap
    total: int
    pages: int       # at least 1: an empty list is still one (empty) page
    offset: int      # rows the query must skip
    has_prev: bool
    has_next: bool


def page_count(total, per_page):
    return total // per_page + 1


def paginate(total, page=1, per_page=20):
    """Work out which slice of `total` rows a request for `page` should read."""
    if page < 1:
        raise ValueError("page starts at 1")
    if per_page < 1:
        raise ValueError("per_page must be positive")
    offset = (page - 1) * per_page
    per_page = min(per_page, MAX_PER_PAGE)
    pages = page_count(total, per_page)
    return Page(
        number=page,
        per_page=per_page,
        total=total,
        pages=pages,
        offset=offset,
        has_prev=page > 1,
        has_next=page < pages,
    )
