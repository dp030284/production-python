from click.testing import CliRunner

from salesreport.cli import cli
from salesreport.report import validate_sales_rows

CSV = """store_id,date,item,quantity,unit_price
S001,2026-07-01,widget-a,12,9.99
,2026-07-01,widget-b,4,19.99
S002,2026-07-01,widget-a,,9.99
S002,2026-07-01,widget-c,lots,4.50
S003,2026-07-01,widget-c,20,4.50
S003,2026-07-01,widget-c,20,four
"""


def test_validate_sales_rows_flags_bad_rows():
    rows = [
        {"store_id": "S001", "quantity": "3"},
        {"store_id": "", "quantity": "3"},
        {"store_id": "S002", "quantity": " "},
        {"store_id": "S002", "quantity": "2.5"},
    ]
    valid, skipped = validate_sales_rows(rows)
    assert valid == [rows[0]]
    assert skipped == [
        (3, "missing store_id"),
        (4, "missing quantity"),
        (5, "malformed quantity '2.5'"),
    ]


def test_validate_command_reports_skipped_rows(tmp_path):
    path = tmp_path / "sales.csv"
    path.write_text(CSV)
    result = CliRunner().invoke(cli, ["validate", "--input", str(path)])
    assert result.exit_code == 1
    assert "3 valid row(s), 3 skipped." in result.output
    assert "line 3: missing store_id" in result.output
    assert "line 4: missing quantity" in result.output
    assert "line 5: malformed quantity 'lots'" in result.output


def test_validate_command_passes_clean_file(tmp_path):
    path = tmp_path / "sales.csv"
    path.write_text("store_id,quantity,unit_price\nS001,1,2.00\n")
    result = CliRunner().invoke(cli, ["validate", "--input", str(path)])
    assert result.exit_code == 0
    assert "1 valid row(s), 0 skipped." in result.output
