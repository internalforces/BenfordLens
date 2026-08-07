"""Main application window: file open, manual column selection, analyze, chart.

Column selection is always an explicit user click on a table row — this
module never auto-picks or auto-analyzes a column, per AGENTS.md.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from PySide6.QtCore import QEvent, Qt, QTimer, QTranslator
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QBoxLayout,
    QComboBox,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QInputDialog,
    QLayout,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from benford_lens.analysis.benford import BenfordResult, CombinedBenfordResult, DigitPosition
from benford_lens.analysis.expert_statistics import CombinedExpertStatistics, ExpertStatistics
from benford_lens.analysis.suitability import SuitabilityAssessment
from benford_lens.charts.benford_chart import (
    SUMMARY_CLOSE_TO_BENFORD,
    SUMMARY_DIVERGES_FROM_BENFORD,
    SUMMARY_NO_VALID_VALUES,
    SUMMARY_SAMPLE_TOO_SMALL,
    ResultSummary,
    build_digit_figure,
    build_first_digit_figure,
    summarize_result,
)
from benford_lens.report.html_report import ReportContext, render_html_report
from benford_lens.ui.controller import AnalysisMode, AnalysisSnapshot, SessionController
from benford_lens.ui.digit_result_panel import DigitResultPanel
from benford_lens.ui.drill_down_panel import DrillDownPanel
from benford_lens.ui.expert_statistics_panel import ExpertStatisticsPanel
from benford_lens.ui.preprocessing_panel import PreprocessingPanel
from benford_lens.ui.suitability_panel import SuitabilityPanel


def _i18n_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS) / "resources" / "i18n"  # type: ignore[attr-defined]
    return Path(__file__).resolve().parents[3] / "resources" / "i18n"


_LANGUAGES = [
    ("en", "English"),
    ("ko", "한국어"),
    ("zh", "中文"),
    ("ja", "日本語"),
    ("es", "Español"),
    ("fr", "Français"),
    ("ru", "Русский"),
]

_UI_FONT_FAMILIES = {
    "ko": (
        "Malgun Gothic",
        "Apple SD Gothic Neo",
        "Noto Sans CJK KR",
    ),
    "zh": (
        "Microsoft YaHei UI",
        "Microsoft YaHei",
        "Microsoft JhengHei UI",
        "Microsoft JhengHei",
        "PingFang SC",
        "Noto Sans CJK SC",
    ),
    "ja": (
        "Yu Gothic UI",
        "Yu Gothic",
        "Meiryo UI",
        "Meiryo",
        "Hiragino Sans",
        "Noto Sans CJK JP",
    ),
}


def _font_for_language(base_font: QFont, language_code: str) -> QFont:
    """Return a copy with platform CJK fallbacks suitable for the UI locale."""
    font = QFont(base_font)
    candidates = _UI_FONT_FAMILIES.get(language_code)
    if candidates is not None:
        font.setFamilies([*candidates, *base_font.families()])
    return font


class _ResponsiveResultsWidget(QWidget):
    """Keep combined charts readable across compact and wide viewports."""

    _WIDE_LAYOUT_MINIMUM = 1100
    _COMPACT_LAYOUT_MAXIMUM = 1000

    def __init__(self, first_panel: QWidget, second_panel: QWidget) -> None:
        super().__init__()
        self.results_layout = QBoxLayout(QBoxLayout.Direction.TopToBottom)
        self.results_layout.setContentsMargins(0, 0, 0, 0)
        self.results_layout.addWidget(first_panel)
        self.results_layout.addWidget(second_panel)
        self.setLayout(self.results_layout)

    def resizeEvent(self, event) -> None:
        """Switch orientation with hysteresis so scrollbars cannot cause oscillation."""
        width = event.size().width()
        direction = self.results_layout.direction()
        if direction is QBoxLayout.Direction.TopToBottom and width >= self._WIDE_LAYOUT_MINIMUM:
            self.results_layout.setDirection(QBoxLayout.Direction.LeftToRight)
        elif direction is QBoxLayout.Direction.LeftToRight and width < self._COMPACT_LAYOUT_MAXIMUM:
            self.results_layout.setDirection(QBoxLayout.Direction.TopToBottom)
        super().resizeEvent(event)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        app = QApplication.instance()
        assert isinstance(app, QApplication)
        self._default_application_font = QFont(app.font())
        self.setWindowTitle(self.tr("Benford Lens"))
        self.controller = SessionController()
        # Column identities for the current file, in the same order as the
        # column table's rows. Row -> identity lookups must go through this
        # list rather than through QTableWidgetItem.text(): pd.read_excel can
        # yield non-string column labels (e.g. int headers like 2021), and
        # str(column) is not guaranteed to round-trip back to the original
        # value, which would break equality checks against df.columns.
        self._columns: list[Any] = []

        self.column_table = QTableWidget(0, 2)
        self.column_table.setHorizontalHeaderLabels([self.tr("Column"), self.tr("Type")])
        self.column_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.column_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.column_table.itemSelectionChanged.connect(self._on_column_selected)

        self.open_button = QPushButton(self.tr("Open File…"))
        self.open_button.clicked.connect(self._on_open_clicked)

        self._source_path: str | None = None

        self.analyze_button = QPushButton(self.tr("Analyze"))
        self.analyze_button.setEnabled(False)
        self.analyze_button.clicked.connect(self._on_analyze_clicked)

        self.mode_combo = QComboBox()
        self._populate_mode_combo()
        self.mode_combo.currentIndexChanged.connect(self._on_analysis_mode_changed)

        self.export_report_button = QPushButton(self.tr("Export Report…"))
        self.export_report_button.setEnabled(False)
        self.export_report_button.clicked.connect(self._on_export_report_clicked)

        self._translator: QTranslator | None = None
        self.language_combo = QComboBox()
        for code, label in _LANGUAGES:
            self.language_combo.addItem(label, code)
            item_index = self.language_combo.count() - 1
            item_font = _font_for_language(self._default_application_font, code)
            self.language_combo.setItemData(item_index, item_font, Qt.ItemDataRole.FontRole)
        self.language_combo.currentIndexChanged.connect(
            lambda _index: self._switch_language(self.language_combo.currentData())
        )

        self.preprocessing_panel = PreprocessingPanel(
            self._on_preprocessing_preview_requested,
            self._on_preprocessing_option_changed,
        )
        self.preprocessing_panel.setEnabled(False)

        self.suitability_panel = SuitabilityPanel()
        self.expert_statistics_panel = ExpertStatisticsPanel()
        self.drill_down_panel = DrillDownPanel()

        self.first_result_panel = DigitResultPanel(DigitPosition.FIRST)
        self.second_result_panel = DigitResultPanel(DigitPosition.SECOND)
        self.first_result_panel.digit_clicked.connect(self._on_result_digit_clicked)
        self.second_result_panel.digit_clicked.connect(self._on_result_digit_clicked)
        # Compatibility alias for existing callers/tests that read the
        # original first-mode summary label directly.
        self.summary_label = self.first_result_panel.summary_label
        self.first_result_panel.set_prompt(self.tr("Open a CSV or Excel file to begin."))
        self.second_result_panel.hide()

        self.results_widget = _ResponsiveResultsWidget(
            self.first_result_panel, self.second_result_panel
        )
        # Kept as a direct view for UI tests and callers that need to inspect
        # the current responsive direction.
        self.results_layout = self.results_widget.results_layout

        top_bar = QHBoxLayout()
        top_bar.addWidget(self.open_button)
        top_bar.addWidget(self.mode_combo)
        top_bar.addWidget(self.analyze_button)
        top_bar.addWidget(self.export_report_button)
        top_bar.addWidget(self.language_combo)

        workflow_layout = QVBoxLayout()
        workflow_layout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        workflow_layout.addWidget(self.column_table)
        workflow_layout.addWidget(self.preprocessing_panel)
        workflow_layout.addWidget(self.suitability_panel)
        workflow_layout.addWidget(self.results_widget)
        workflow_layout.addWidget(self.expert_statistics_panel)
        workflow_layout.addWidget(self.drill_down_panel)

        self.workflow_widget = QWidget()
        self.workflow_widget.setLayout(workflow_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setWidget(self.workflow_widget)

        layout = QVBoxLayout()
        layout.addLayout(top_bar)
        layout.addWidget(self.scroll_area, 1)

        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)

    @property
    def canvas(self):
        """Compatibility view of the primary chart canvas for the active mode."""
        mode = self.controller.state.analysis_mode
        if mode is AnalysisMode.SECOND:
            return self.second_result_panel.canvas
        return self.first_result_panel.canvas

    def _mode_labels(self) -> dict[AnalysisMode, str]:
        return {
            AnalysisMode.FIRST: self.tr("First digit"),
            AnalysisMode.SECOND: self.tr("Second digit"),
            AnalysisMode.COMBINED: self.tr("First + second"),
        }

    def _populate_mode_combo(self) -> None:
        current_mode = self.controller.state.analysis_mode
        self.mode_combo.blockSignals(True)
        self.mode_combo.clear()
        for mode, label in self._mode_labels().items():
            self.mode_combo.addItem(label, mode.value)
        self.mode_combo.setCurrentIndex(self.mode_combo.findData(current_mode.value))
        self.mode_combo.blockSignals(False)

    def _selected_analysis_mode(self) -> AnalysisMode:
        return AnalysisMode(self.mode_combo.currentData())

    def _on_analysis_mode_changed(self, _index: int) -> None:
        mode = self._selected_analysis_mode()
        self.controller.set_analysis_mode(mode)
        self._invalidate_analyzed_state()
        self._set_workflow_prompt()

    def _set_result_panel_visibility(self, mode: AnalysisMode) -> None:
        self.first_result_panel.setVisible(mode in (AnalysisMode.FIRST, AnalysisMode.COMBINED))
        self.second_result_panel.setVisible(mode in (AnalysisMode.SECOND, AnalysisMode.COMBINED))

    def _set_workflow_prompt(self) -> None:
        state = self.controller.state
        if state.dataframe is None:
            prompt = self.tr("Open a CSV or Excel file to begin.")
        else:
            prompt = self.tr("Select a column, then click Analyze.")
        mode = state.analysis_mode
        self._set_result_panel_visibility(mode)
        if mode is AnalysisMode.SECOND:
            self.second_result_panel.set_prompt(prompt)
        else:
            self.first_result_panel.set_prompt(prompt)
            if mode is AnalysisMode.COMBINED:
                self.second_result_panel.set_prompt(prompt)

    def _on_open_clicked(self) -> None:
        path, _selected_filter = QFileDialog.getOpenFileName(
            self,
            self.tr("Open data file"),
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
                        self, self.tr("Select sheet"), self.tr("Sheet:"), sheets, 0, False
                    )
                    if not ok:
                        return
                self.controller.open_excel(path, sheet_name)
            else:
                self.controller.open_csv(path)
        except Exception as exc:
            QMessageBox.critical(self, self.tr("Could not open file"), str(exc))
            return
        # Commit the report's source identity only after the new dataframe is
        # open. Cancelling sheet selection or hitting a load error leaves the
        # previous analysis intact, so its source name must remain intact too.
        self._source_path = path
        self._populate_columns()

    def _populate_columns(self) -> None:
        dataframe = self.controller.state.dataframe
        self.column_table.clearSelection()
        self.column_table.setRowCount(0)
        self.analyze_button.setEnabled(False)
        self.preprocessing_panel.setEnabled(False)
        # SessionController resets state.preprocessing_options for every new
        # file, so the panel has to follow — otherwise it would show the
        # previous file's selections while the controller used the defaults.
        self.preprocessing_panel.reset_to_defaults()
        self.suitability_panel.clear()
        self._columns = []
        self._invalidate_analyzed_state()
        if dataframe is None:
            return
        self.column_table.setRowCount(len(dataframe.columns))
        for row, column in enumerate(dataframe.columns):
            self._columns.append(column)
            self.column_table.setItem(row, 0, QTableWidgetItem(str(column)))
            self.column_table.setItem(row, 1, QTableWidgetItem(str(dataframe[column].dtype)))
        self._set_workflow_prompt()

    def _on_column_selected(self) -> None:
        selected_rows = self.column_table.selectionModel().selectedRows()
        if not selected_rows:
            self.analyze_button.setEnabled(False)
            return
        try:
            column = self._columns[selected_rows[0].row()]
            self.controller.select_column(column)
        except Exception as exc:
            QMessageBox.critical(self, self.tr("Cannot select column"), str(exc))
            return
        self.analyze_button.setEnabled(True)
        self.preprocessing_panel.setEnabled(True)
        # A previously rendered chart (and its clickable digit bars) belongs to
        # whichever column/options were active at analyze() time — see Task 11
        # final review.
        self._invalidate_analyzed_state()
        self._set_workflow_prompt()
        self._update_suitability()

    def _on_analyze_clicked(self) -> None:
        self.controller.configure_preprocessing(self.preprocessing_panel.current_options())
        try:
            self.controller.analyze(self._selected_analysis_mode())
        except Exception as exc:
            QMessageBox.warning(self, self.tr("Cannot analyze"), str(exc))
            return
        snapshot = self.controller.state.analysis_snapshot
        if snapshot is None:  # pragma: no cover - controller always snapshots successful runs
            return
        self._render_snapshot(snapshot)
        # Show the exact assessment analyze() snapshotted into
        # last_suitability, not a fresh check_suitability() recompute — the
        # on-screen panel must always match what a report export would embed
        # for this analysis, with no room for the two to diverge.
        self._update_suitability(self.controller.state.last_suitability)
        self.export_report_button.setEnabled(True)
        QTimer.singleShot(0, self._scroll_to_results)

    def _scroll_to_results(self) -> None:
        """Bring the newly rendered result into view without hiding overflow."""
        self.scroll_area.ensureWidgetVisible(self.results_widget, 0, 20)

    def _render_snapshot(self, snapshot: AnalysisSnapshot) -> None:
        """Render every result and statistic from one controller snapshot."""
        self._set_result_panel_visibility(snapshot.mode)
        observed_label = self.tr("Observed")
        expected_label = self.tr("Expected (Benford)")

        if isinstance(snapshot.result, CombinedBenfordResult):
            self._show_result_panel(
                self.first_result_panel,
                snapshot.result.first,
                DigitPosition.FIRST,
                observed_label,
                expected_label,
            )
            self._show_result_panel(
                self.second_result_panel,
                snapshot.result.second,
                DigitPosition.SECOND,
                observed_label,
                expected_label,
            )
        else:
            position = (
                DigitPosition.FIRST if snapshot.mode is AnalysisMode.FIRST else DigitPosition.SECOND
            )
            panel = (
                self.first_result_panel
                if position is DigitPosition.FIRST
                else self.second_result_panel
            )
            self._show_result_panel(
                panel,
                snapshot.result,
                position,
                observed_label,
                expected_label,
            )

        statistics = snapshot.expert_statistics
        if isinstance(statistics, CombinedExpertStatistics):
            self.expert_statistics_panel.show_combined_statistics(statistics)
        elif isinstance(statistics, ExpertStatistics):
            self.expert_statistics_panel.show_statistics(statistics)

    def _show_result_panel(
        self,
        panel: DigitResultPanel,
        result: BenfordResult,
        position: DigitPosition,
        observed_label: str,
        expected_label: str,
    ) -> None:
        position_label = (
            self.tr("First digit") if position is DigitPosition.FIRST else self.tr("Second digit")
        )
        panel.show_result(
            result,
            title=self.tr("{position} analysis").format(position=position_label),
            summary=f"{position_label}: {self._summary_text(summarize_result(result))}",
            x_axis_label=position_label,
            y_axis_label=self.tr("Proportion (%)"),
            observed_label=observed_label,
            expected_label=expected_label,
        )

    def _summary_templates(self) -> dict[str, str]:
        """Translatable template per result-summary code.

        Wording is neutral and exploratory per AGENTS.md and directs users to
        interpret the comparison alongside the characteristics of the data.
        """
        return {
            SUMMARY_NO_VALID_VALUES: self.tr(
                "No valid numeric values were found in the selected column."
            ),
            SUMMARY_SAMPLE_TOO_SMALL: self.tr(
                "Only {sample_size} valid numeric value(s) were found, which is too few for a "
                "meaningful comparison to the expected Benford distribution. "
                "Try a column with more data."
            ),
            SUMMARY_CLOSE_TO_BENFORD: self.tr(
                "The overall distribution is close to the expected Benford distribution. "
                "Interpret this comparison together with the characteristics of the data."
            ),
            SUMMARY_DIVERGES_FROM_BENFORD: self.tr(
                "The overall distribution differs somewhat from the expected Benford "
                "distribution. Further review of the data characteristics may be warranted."
            ),
        }

    def _summary_text(self, summary: ResultSummary) -> str:
        template = self._summary_templates().get(summary.code)
        if template is None:  # pragma: no cover - defensive, every code is mapped
            return summary.code
        return template.format(**summary.params)

    def _on_export_report_clicked(self) -> None:
        # Everything in the report comes from the snapshot analyze() took, so
        # the preprocessing summary, the suitability badge and the digit table
        # always describe the same single analysis — never a mix of the live
        # panel selection and an older result.
        state = self.controller.state
        snapshot = state.analysis_snapshot
        if snapshot is None:
            return
        source_name = Path(self._source_path).name if self._source_path else ""
        if isinstance(snapshot.result, CombinedBenfordResult):
            context = ReportContext(
                source_name=source_name,
                column_name=state.selected_column,
                sheet_name=state.sheet_name,
                preprocessing_options=snapshot.preprocessing_options,
                preprocessing_preview=snapshot.preprocessing_preview,
                suitability=snapshot.suitability,
                expert_statistics=snapshot.expert_statistics,
                mode="combined",
                result=snapshot.result.first,
                result_summary=summarize_result(snapshot.result.first),
                chart_figure=build_first_digit_figure(snapshot.result.first),
                second_result=snapshot.result.second,
                second_result_summary=summarize_result(snapshot.result.second),
                second_chart_figure=build_digit_figure(
                    snapshot.result.second, x_axis_label="Second digit"
                ),
            )
        elif snapshot.mode is AnalysisMode.FIRST:
            context = ReportContext(
                source_name=source_name,
                column_name=state.selected_column,
                sheet_name=state.sheet_name,
                preprocessing_options=snapshot.preprocessing_options,
                preprocessing_preview=snapshot.preprocessing_preview,
                suitability=snapshot.suitability,
                expert_statistics=snapshot.expert_statistics,
                mode="first",
                result=snapshot.result,
                result_summary=summarize_result(snapshot.result),
                chart_figure=build_first_digit_figure(snapshot.result),
            )
        else:
            context = ReportContext(
                source_name=source_name,
                column_name=state.selected_column,
                sheet_name=state.sheet_name,
                preprocessing_options=snapshot.preprocessing_options,
                preprocessing_preview=snapshot.preprocessing_preview,
                suitability=snapshot.suitability,
                expert_statistics=snapshot.expert_statistics,
                mode="second",
                result=snapshot.result,
                result_summary=summarize_result(snapshot.result),
                chart_figure=build_digit_figure(snapshot.result, x_axis_label="Second digit"),
            )
        html = render_html_report(context)

        path, _selected_filter = QFileDialog.getSaveFileName(
            self, self.tr("Export report"), "", "HTML files (*.html)"
        )
        if not path:
            return
        try:
            Path(path).write_text(html, encoding="utf-8")
        except Exception as exc:
            QMessageBox.critical(self, self.tr("Could not export report"), str(exc))

    def _on_preprocessing_preview_requested(self, options) -> None:
        preview = self.controller.configure_preprocessing(options)
        self.preprocessing_panel.show_preview(preview)
        self._update_suitability()
        self._invalidate_analyzed_state()

    def _invalidate_analyzed_state(self) -> None:
        """Drop on-screen analysis output that no longer matches the settings.

        Charts, report export, expert details, and raw rows all belong to one
        controller snapshot and therefore disappear together when its inputs
        change.
        """
        self.export_report_button.setEnabled(False)
        self.expert_statistics_panel.clear()
        self._clear_chart()
        self.drill_down_panel.clear()

    def _on_preprocessing_option_changed(self) -> None:
        """Handle a combo edited directly, without going through Preview.

        Distinct from `_on_preprocessing_preview_requested`, which also
        invalidates analyzed state but must NOT blank the preview label it
        just populated. This path fires only on a raw combo change, so the
        stale preview text (describing the previous combo selection) is
        cleared here instead.
        """
        try:
            self.controller.configure_preprocessing(self.preprocessing_panel.current_options())
        except Exception:
            pass
        self._invalidate_analyzed_state()
        self._set_workflow_prompt()
        self.preprocessing_panel.clear_preview()

    def _update_suitability(self, assessment: SuitabilityAssessment | None = None) -> None:
        """Refresh the suitability panel.

        With no argument, recomputes live from the current column/options —
        used before any analysis has run (e.g. right after column selection)
        or during a Preview, where there is no analyze() snapshot yet to
        display instead. When called with an assessment (from
        `state.last_suitability` right after analyze()), that exact object is
        shown instead of recomputing, so the panel can never diverge from
        what a report export would embed for the same analysis.
        """
        if assessment is None:
            try:
                assessment = self.controller.check_suitability()
            except Exception:
                return
        self.suitability_panel.show_assessment(assessment)

    def _clear_chart(self) -> None:
        self.first_result_panel.clear()
        self.second_result_panel.clear()

    def _render_chart(self, result: BenfordResult) -> None:
        """Render the legacy first-digit view (compatibility wrapper)."""
        self._show_result_panel(
            self.first_result_panel,
            result,
            DigitPosition.FIRST,
            self.tr("Observed"),
            self.tr("Expected (Benford)"),
        )

    def _on_chart_clicked(self, event) -> None:
        """Handle a legacy first-chart click (compatibility wrapper)."""
        result = self.first_result_panel.result
        if result is None or event.xdata is None:
            return
        digit = round(event.xdata)
        if digit not in result.expected_proportions:
            return
        self._on_result_digit_clicked(DigitPosition.FIRST, int(digit))

    def _on_result_digit_clicked(self, position: DigitPosition, digit: int) -> None:
        try:
            rows = self.controller.drill_down_digit(position, digit)
        except Exception as exc:
            QMessageBox.warning(self, self.tr("Cannot show rows"), str(exc))
            return
        position_label = (
            self.tr("First digit") if position is DigitPosition.FIRST else self.tr("Second digit")
        )
        self.drill_down_panel.show_rows(rows, f"{position_label}: {digit}")

    def _switch_language(self, language_code: str) -> None:
        app = QApplication.instance()
        assert isinstance(app, QApplication)
        app.setFont(_font_for_language(self._default_application_font, language_code))
        if self._translator is not None:
            app.removeTranslator(self._translator)
            self._translator = None
        if language_code != "en":
            translator = QTranslator()
            translator.load(str(_i18n_dir() / f"benford_lens_{language_code}.qm"))
            app.installTranslator(translator)
            self._translator = translator
        self._retranslate_ui()

    def changeEvent(self, event) -> None:
        if event.type() == QEvent.Type.LanguageChange:
            self._retranslate_ui()
        super().changeEvent(event)

    def _retranslate_ui(self) -> None:
        self.setWindowTitle(self.tr("Benford Lens"))
        self.column_table.setHorizontalHeaderLabels([self.tr("Column"), self.tr("Type")])
        self.open_button.setText(self.tr("Open File…"))
        self.analyze_button.setText(self.tr("Analyze"))
        self.export_report_button.setText(self.tr("Export Report…"))
        self._populate_mode_combo()
        self.suitability_panel.retranslate_ui()
        self.expert_statistics_panel.retranslate_ui()
        self.preprocessing_panel.retranslate_ui()
        self.drill_down_panel.retranslate_ui()
        self._retranslate_summary_label()

    def _retranslate_summary_label(self) -> None:
        """Restore summary_label in the current language, whatever stage we're at.

        It used to be reset unconditionally to the "open a file" prompt, which
        wrongly replaced the "select a column" prompt if the user switched
        language after picking a column but before analyzing.
        """
        state = self.controller.state
        if state.analysis_snapshot is not None:
            self._render_snapshot(state.analysis_snapshot)
        else:
            self._set_workflow_prompt()
