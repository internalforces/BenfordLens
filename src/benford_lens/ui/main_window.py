"""Main application window: file open, manual column selection, analyze, chart.

Column selection is always an explicit user click on a table row — this
module never auto-picks or auto-analyzes a column, per AGENTS.md.
"""

from __future__ import annotations

from typing import Any

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
from benford_lens.ui.preprocessing_panel import PreprocessingPanel
from benford_lens.ui.suitability_panel import SuitabilityPanel


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Benford Lens")
        self.controller = SessionController()
        self.canvas: FigureCanvasQTAgg | None = None
        # Column identities for the current file, in the same order as the
        # column table's rows. Row -> identity lookups must go through this
        # list rather than through QTableWidgetItem.text(): pd.read_excel can
        # yield non-string column labels (e.g. int headers like 2021), and
        # str(column) is not guaranteed to round-trip back to the original
        # value, which would break equality checks against df.columns.
        self._columns: list[Any] = []

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

        self.preprocessing_panel = PreprocessingPanel(self._on_preprocessing_preview_requested)
        self.preprocessing_panel.setEnabled(False)

        self.suitability_panel = SuitabilityPanel()

        self.summary_label = QLabel("Open a CSV or Excel file to begin.")
        self.summary_label.setWordWrap(True)

        self.chart_container = QVBoxLayout()

        top_bar = QHBoxLayout()
        top_bar.addWidget(self.open_button)
        top_bar.addWidget(self.analyze_button)

        layout = QVBoxLayout()
        layout.addLayout(top_bar)
        layout.addWidget(self.column_table)
        layout.addWidget(self.preprocessing_panel)
        layout.addWidget(self.suitability_panel)
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
        self.preprocessing_panel.setEnabled(False)
        self._columns = []
        self._clear_chart()
        if dataframe is None:
            return
        self.column_table.setRowCount(len(dataframe.columns))
        for row, column in enumerate(dataframe.columns):
            self._columns.append(column)
            self.column_table.setItem(row, 0, QTableWidgetItem(str(column)))
            self.column_table.setItem(row, 1, QTableWidgetItem(str(dataframe[column].dtype)))
        self.summary_label.setText("Select a column, then click Analyze.")

    def _on_column_selected(self) -> None:
        selected_rows = self.column_table.selectionModel().selectedRows()
        if not selected_rows:
            self.analyze_button.setEnabled(False)
            return
        try:
            column = self._columns[selected_rows[0].row()]
            self.controller.select_column(column)
        except Exception as exc:
            QMessageBox.critical(self, "Cannot select column", str(exc))
            return
        self.analyze_button.setEnabled(True)
        self.preprocessing_panel.setEnabled(True)
        self._update_suitability()

    def _on_analyze_clicked(self) -> None:
        self.controller.configure_preprocessing(self.preprocessing_panel.current_options())
        try:
            result = self.controller.analyze()
        except Exception as exc:
            QMessageBox.warning(self, "Cannot analyze", str(exc))
            return
        self._render_chart(result)
        self.summary_label.setText(summarize_result(result))

    def _on_preprocessing_preview_requested(self, options) -> None:
        preview = self.controller.configure_preprocessing(options)
        self.preprocessing_panel.show_preview(preview)
        self._update_suitability()

    def _update_suitability(self) -> None:
        try:
            assessment = self.controller.check_suitability()
        except Exception:
            return
        self.suitability_panel.show_assessment(assessment)

    def _clear_chart(self) -> None:
        if self.canvas is not None:
            self.chart_container.removeWidget(self.canvas)
            self.canvas.deleteLater()
            self.canvas = None

    def _render_chart(self, result: BenfordResult) -> None:
        self._clear_chart()
        figure = build_first_digit_figure(result)
        self.canvas = FigureCanvasQTAgg(figure)
        self.chart_container.addWidget(self.canvas)
