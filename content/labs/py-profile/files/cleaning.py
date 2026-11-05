"""Row cleaning shared by the nightly jobs."""


def normalise(row):
    return {
        **row,
        "customer": row["customer"].strip().lower(),
        "region": row["region"].strip().lower(),
    }


def is_new(seen, key):
    return key not in seen


def drop_duplicates(rows):
    """Keep the first row seen for each order_id, in the original order."""
    kept = []
    seen = []
    for row in rows:
        if not is_new(seen, row["order_id"]):
            continue
        seen.append(row["order_id"])
        kept.append(row)
    return kept


def prepare(rows):
    return drop_duplicates([normalise(row) for row in rows])
