"""Command-line entry point for salesreport.

This is the *only* file that should know about argv, click, or how a
human invokes this tool. Everything it does is delegate to report.py -
that's the whole point of separating the two.
"""

from pathlib import Path

import click

from salesreport.report import (
    read_sales_rows,
    total_revenue_by_store,
    validate_sales_rows,
)

@click.group()
def cli():
    """Sales report command-line tool."""
@cli.command()
@click.option(
    "--input",
    "input_path",
    required=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="Path to a CSV file containing sales data.",
)
def generate(input_path: Path) -> None:
    """Print total revenue per store from a sales CSV file."""
    rows = read_sales_rows(input_path)
    totals = total_revenue_by_store(rows)
    click.echo("Revenue by store:")
    for store, total in sorted(totals.items()):
        click.echo(f"  {store}: ${total:.2f}")


@cli.command()
@click.option(
    "--input",
    "input_path",
    required=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="Path to a CSV file containing sales data.",
)
def validate(input_path: Path) -> None:
    """Check a sales CSV for missing or malformed rows."""
    rows = read_sales_rows(input_path)
    valid, skipped = validate_sales_rows(rows)
    click.echo(f"{len(valid)} valid row(s), {len(skipped)} skipped.")
    for line_no, reason in skipped:
        click.echo(f"  line {line_no}: {reason}")
    if skipped:
        raise SystemExit(1)

if __name__ == "__main__":
    cli()