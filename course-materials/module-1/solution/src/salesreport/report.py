"""Core sales-report logic.

Notice this module knows nothing about the CLI, argv, or hardcoded
paths. It takes a path in, and gives data back. That separation is what
makes it testable without touching a filesystem full of magic assumptions,
and reusable from anywhere - a script, a test, a future pipeline step -
not just from one specific folder on one specific machine.
"""

import csv
from pathlib import Path


def read_sales_rows(path : Path) -> list[dict[str, str]]:
    rows = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def total_revenue_by_store(rows: list[dict[str, str]]) -> dict[str, float]:
    totals = {}
    for row in rows:
        store = row["store_id"]
        qty = int(row["quantity"])
        price = float(row["unit_price"])
        totals[store] = totals.get(store, 0.0) + qty * price
    return totals


def validate_sales_rows(
    rows: list[dict[str, str]],
) -> tuple[list[dict[str, str]], list[tuple[int, str]]]:
    """Split rows into valid rows and (line_number, reason) for invalid ones.

    A row is invalid if store_id or quantity is missing/blank, or if
    quantity isn't a whole number (generate() parses it with int()).
    Line numbers refer to the CSV file, where line 1 is the header.
    """
    valid: list[dict[str, str]] = []
    skipped: list[tuple[int, str]] = []
    for line_no, row in enumerate(rows, start=2):
        store = (row.get("store_id") or "").strip()
        qty = (row.get("quantity") or "").strip()
        if not store:
            skipped.append((line_no, "missing store_id"))
        elif not qty:
            skipped.append((line_no, "missing quantity"))
        else:
            try:
                int(qty)
            except ValueError:
                skipped.append((line_no, f"malformed quantity {qty!r}"))
            else:
                valid.append(row)
    return valid, skipped
