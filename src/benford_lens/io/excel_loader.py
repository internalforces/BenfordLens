"""Excel loading with explicit sheet selection.

Sheet choice is always passed in by the caller (the UI's user-facing sheet
picker) — this module never guesses which sheet to load.
"""

from __future__ import annotations

import pandas as pd


def list_sheets(path: str) -> list[str]:
    """Return the sheet names in an Excel workbook, in file order."""
    with pd.ExcelFile(path) as workbook:
        return list(workbook.sheet_names)


def load_excel(path: str, sheet_name: str) -> pd.DataFrame:
    """Load a single named sheet from an Excel workbook into a DataFrame."""
    return pd.read_excel(path, sheet_name=sheet_name)
