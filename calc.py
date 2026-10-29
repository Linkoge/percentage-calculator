"""Percentage calculation logic (mirrored in static/app.js for live use)."""
from __future__ import annotations

import math


def parse_number(value) -> float | None:
    """Parse user input into a finite float; accepts comma decimals. None if invalid/empty."""
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        n = float(value)
    else:
        text = str(value).strip().replace(" ", "").replace(",", ".")
        if not text:
            return None
        try:
            n = float(text)
        except ValueError:
            return None
    return n if math.isfinite(n) else None


def percentage(amount, total) -> float | None:
    """Percent that `amount` is of `total`; None when either is invalid or total is zero."""
    a, t = parse_number(amount), parse_number(total)
    if a is None or t is None or t == 0:
        return None
    return a / t * 100


def summarize(total, amounts) -> dict:
    """Per-row percentages plus sum/remaining summary."""
    t = parse_number(total)
    valid_total = t is not None and t > 0
    rows = []
    used = 0.0
    for raw in amounts:
        a = parse_number(raw)
        blank = isinstance(raw, str) and not raw.strip() or raw is None
        rows.append({
            "amount": a,
            "percent": percentage(a, t) if valid_total and a is not None else None,
            "valid": a is not None or blank,
        })
        if a is not None:
            used += a
    return {
        "total": t if valid_total else None,
        "valid_total": valid_total,
        "rows": rows,
        "sum": used,
        "sum_percent": used / t * 100 if valid_total else None,
        "remaining": t - used if valid_total else None,
        "remaining_percent": (t - used) / t * 100 if valid_total else None,
        "over": bool(valid_total and used > t),
    }
