"""Raw-row drill-down: shows original rows for a clicked chart digit, with
search and CSV export."""

from __future__ import annotations

import pandas as pd
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class DrillDownPanel(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._rows: pd.DataFrame | None = None

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText(self.tr("Search…"))
        self.search_box.textChanged.connect(self._apply_filter)

        self.export_button = QPushButton(self.tr("Export CSV…"))
        self.export_button.clicked.connect(self._on_export_clicked)

        self.table = QTableWidget(0, 0)

        top_bar = QHBoxLayout()
        top_bar.addWidget(self.search_box)
        top_bar.addWidget(self.export_button)

        layout = QVBoxLayout()
        layout.addLayout(top_bar)
        layout.addWidget(self.table)
        self.setLayout(layout)

    def show_rows(self, rows: pd.DataFrame) -> None:
        self._rows = rows
        self.search_box.clear()
        self._render(rows)

    def _render(self, rows: pd.DataFrame) -> None:
        self.table.setColumnCount(len(rows.columns))
        self.table.setHorizontalHeaderLabels([str(c) for c in rows.columns])
        self.table.setRowCount(len(rows))
        for row_index, (_, row) in enumerate(rows.iterrows()):
            for col_index, value in enumerate(row):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(value)))

    def _apply_filter(self, text: str) -> None:
        if self._rows is None:
            return
        if not text:
            self._render(self._rows)
            return
        mask = self._rows.apply(
            lambda row: row.astype(str).str.contains(text, case=False, na=False).any(), axis=1
        )
        self._render(self._rows[mask])

    def _on_export_clicked(self) -> None:
        if self._rows is None:
            return
        path, _selected_filter = QFileDialog.getSaveFileName(
            self, self.tr("Export rows"), "", "CSV files (*.csv)"
        )
        if not path:
            return
        try:
            self._rows.to_csv(path, index=False)
        except Exception as exc:
            QMessageBox.critical(self, self.tr("Could not export"), str(exc))
