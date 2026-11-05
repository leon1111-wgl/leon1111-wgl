"""Fabricated order export used by the nightly sales report."""
import random

REGIONS = ["north", "south", "east", "west"]
CUSTOMERS = [f"cust-{i:04d}" for i in range(1, 801)]


def make_orders(n, seed=2123):
    """Return n order rows. About one row in ten is a re-sent copy of an earlier order."""
    rng = random.Random(seed)
    rows = []
    for i in range(n):
        if rows and rng.random() < 0.10:
            rows.append(dict(rng.choice(rows)))  # the exporter retried and sent an old order again
            continue
        rows.append({
            "order_id": f"ORD-{i:07d}",
            "customer": rng.choice(CUSTOMERS),
            "region": rng.choice(REGIONS),
            "amount_cents": rng.randrange(500, 40000),
        })
    return rows
