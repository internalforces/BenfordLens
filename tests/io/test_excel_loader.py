import pandas as pd

from benford_lens.io.excel_loader import list_sheets, load_excel


def _write_workbook(path) -> None:
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        pd.DataFrame({"name": ["alice", "bob"], "amount": [120, 45]}).to_excel(
            writer, sheet_name="Transactions", index=False
        )
        pd.DataFrame({"category": ["A", "B"]}).to_excel(writer, sheet_name="Lookup", index=False)


def test_list_sheets_returns_all_sheet_names(tmp_path):
    xlsx_path = tmp_path / "book.xlsx"
    _write_workbook(xlsx_path)

    sheets = list_sheets(str(xlsx_path))

    assert sheets == ["Transactions", "Lookup"]


def test_load_excel_reads_the_requested_sheet(tmp_path):
    xlsx_path = tmp_path / "book.xlsx"
    _write_workbook(xlsx_path)

    df = load_excel(str(xlsx_path), sheet_name="Transactions")

    assert list(df.columns) == ["name", "amount"]
    assert df["amount"].tolist() == [120, 45]


def test_load_excel_reads_a_different_sheet(tmp_path):
    xlsx_path = tmp_path / "book.xlsx"
    _write_workbook(xlsx_path)

    df = load_excel(str(xlsx_path), sheet_name="Lookup")

    assert list(df.columns) == ["category"]
