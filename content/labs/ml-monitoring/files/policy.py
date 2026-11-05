"""Alert policy: turns the monitoring numbers for one window into an action.

`window` has: rows, psi {feature: value}, used {feature: bool, does the model use it},
z (observed late rate against the model's expectation, in standard errors; None before labels arrive)
and gap (observed minus expected late rate, or None).
"""
PSI_LIMIT = 0.10


def decide(window):
    """Return (action, reasons)."""
    over = [f"PSI {value:.2f} on {feature}" for feature, value in window["psi"].items() if value > PSI_LIMIT]
    if over:
        return "PAGE", over
    return "ok", []
