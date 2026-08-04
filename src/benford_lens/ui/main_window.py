"""Main application window: file open, manual column selection, analyze, chart.

Column selection is always an explicit user click on a table row — this
module never auto-picks or auto-analyzes a column, per AGENTS.md.
"""

from __future__ import annotations

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from benford_lens.analysis.benford import BenfordResult
from benford_lens.charts.benford_chart import build_first_digit_figure, summarize_result
from benford_lens.ui.controller import SessionController


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Benford Lens")
        self.controller = SessionController()
        self.canvas: FigureCanvasQTAgg | None = None

        self.column_table = QTableWidget(0, 2)
        self.column_table.setHorizontalHeaderLabels(["Column", "Type"])
        self.column_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.column_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.column_table.itemSelectionChanged.connect(self._on_column_selected)

        self.open_button = QPushButton("Open File…")
        self.open_button.clicked.connect(self._on_open_clicked)

        self.analyze_button = QPushButton("Analyze")
        self.analyze_button.setEnabled(False)
        self.analyze_button.clicked.connect(self._on_analyze_clicked)

        self.summary_label = QLabel("Open a CSV or Excel file to begin.")
        self.summary_label.setWordWrap(True)

        self.chart_container = QVBoxLayout()

        top_bar = QHBoxLayout()
        top_bar.addWidget(self.open_button)
        top_bar.addWidget(self.analyze_button)

        layout = QVBoxLayout()
        layout.addLayout(top_bar)
        layout.addWidget(self.column_table)
        layout.addWidget(self.summary_label)
        layout.addLayout(self.chart_container)

        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)

    def _on_open_clicked(self) -> None:
        path, _selected_filter = QFileDialog.getOpenFileName(
            self,
            "Open data file",
            "",
            "Data files (*.csv *.xlsx);;CSV files (*.csv);;Excel files (*.xlsx)",
        )
        if path:
            self.load_file(path)

    def load_file(self, path: str) -> None:
        try:
            if path.lower().endswith(".xlsx"):
                sheets = self.controller.list_excel_sheets(path)
                sheet_name = sheets[0]
                if len(sheets) > 1:
                    sheet_name, ok = QInputDialog.getItem(
                        self, "Select sheet", "Sheet:", sheets, 0, False
                    )
                    if not ok:
                        return
                self.controller.open_excel(path, sheet_name)
            else:
                self.controller.open_csv(path)
        except Exception as exc:
            QMessageBox.critical(self, "Could not open file", str(exc))
            return
        self._populate_columns()

    def _populate_columns(self) -> None:
        dataframe = self.controller.state.dataframe
        self.column_table.clearSelection()
        self.column_table.setRowCount(0)
        self.analyze_button.setEnabled(False)
        if dataframe is None:
            return
        self.column_table.setRowCount(len(dataframe.columns))
        for row, column in enumerate(dataframe.columns):
            self.column_table.setItem(row, 0, QTableWidgetItem(str(column)))
            self.column_table.setItem(row, 1, QTableWidgetItem(str(dataframe[column].dtype)))
        self.summary_label.setText("Select a column, then click Analyze.")

    def _on_column_selected(self) -> None:
        selected_rows = self.column_table.selectionModel().selectedRows()
        if not selected_rows:
            self.analyze_button.setEnabled(False)
            return
        item = self.column_table.item(selected_rows[0].row(), 0)
        assert item is not None
        column_name = item.text()
        self.controller.select_column(column_name)
        self.analyze_button.setEnabled(True)

    def _on_analyze_clicked(self) -> None:
        try:
            result = self.controller.analyze()
        except ValueError as exc:
            QMessageBox.warning(self, "Cannot analyze", str(exc))
            return
        self._render_chart(result)
        self.summary_label.setText(summarize_result(result))

    def _render_chart(self, result: BenfordResult) -> None:
        if self.canvas is not None:
            self.chart_container.removeWidget(self.canvas)
            self.canvas.deleteLater()
        figure = build_first_digit_figure(result)
        self.canvas = FigureCanvasQTAgg(figure)
        self.chart_container.addWidget(self.canvas)
