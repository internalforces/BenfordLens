from types import SimpleNamespace

import pandas as pd
import pytest
from PySide6.QtCore import Qt
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication

from benford_lens.analysis.preprocessing import PreprocessingOptions
from benford_lens.ui.main_window import MainWindow


@pytest.fixture
def app():
    application = QApplication.instance() or QApplication([])
    yield application


@pytest.fixture
def window(app):
    win = MainWindow()
    yield win
    # QTranslator instances are installed on the shared QApplication, so a
    # test that switches language would otherwise leak it into every test
    # that runs after it.
    win._switch_language("en")
    win.close()


def _write_csv(tmp_path):
    path = tmp_path / "data.csv"
    path.write_text("name,amount\nalice,111\nbob,222\ncarol,111\n", encoding="utf-8")
    return str(path)


def _write_single_sheet_excel(tmp_path):
    path = tmp_path / "single_sheet.xlsx"
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        pd.DataFrame({"name": ["alice", "bob"], "amount": [120, 45]}).to_excel(
            writer, sheet_name="Data", index=False
        )
    return str(path)


def _write_multi_sheet_excel_with_numeric_headers(tmp_path):
    # Regression fixture for Finding 1: the second sheet's header row is
    # numeric (year columns), which pandas reads as int column labels, not
    # str — the exact case that broke str(column)-round-trip column
    # selection via the table's display text.
    path = tmp_path / "multi_sheet.xlsx"
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        pd.DataFrame({"name": ["alice", "bob"]}).to_excel(writer, sheet_name="Lookup", index=False)
        pd.DataFrame({2021: [111, 111, 222], 2022: [4, 5, 6]}).to_excel(
            writer, sheet_name="Yearly", index=False
        )
    return str(path)


def test_load_file_populates_the_column_table(window, tmp_path):
    window.load_file(_write_csv(tmp_path))

    assert window.column_table.rowCount() == 2
    assert window.column_table.item(0, 0).text() == "name"
    assert window.column_table.item(1, 0).text() == "amount"


def test_analyze_button_disabled_until_a_column_is_selected(window, tmp_path):
    window.load_file(_write_csv(tmp_path))

    assert window.analyze_button.isEnabled() is False

    window.column_table.selectRow(1)

    assert window.analyze_button.isEnabled() is True
    assert window.controller.state.selected_column == "amount"


def test_analyze_renders_chart_and_summary(window, tmp_path):
    window.load_file(_write_csv(tmp_path))
    window.column_table.selectRow(1)

    window._on_analyze_clicked()

    assert window.canvas is not None
    assert window.summary_label.text() != ""


def test_clicking_a_data_cell_selects_the_whole_row(window, tmp_path):
    window.load_file(_write_csv(tmp_path))

    index = window.column_table.model().index(1, 0)
    cell_center = window.column_table.visualRect(index).center()
    QTest.mouseClick(window.column_table.viewport(), Qt.MouseButton.LeftButton, pos=cell_center)

    assert window.analyze_button.isEnabled() is True
    assert window.controller.state.selected_column == "amount"


def test_load_file_shows_error_dialog_on_bad_path(window, tmp_path, monkeypatch):
    shown = {}

    def fake_critical(parent, title, text):
        shown["title"] = title
        shown["text"] = text

    monkeypatch.setattr("benford_lens.ui.main_window.QMessageBox.critical", fake_critical)

    window.load_file(str(tmp_path / "missing.csv"))

    assert shown["title"] == "Could not open file"
    assert window.column_table.rowCount() == 0


def test_load_file_single_sheet_excel_populates_columns_without_dialog(
    window, tmp_path, monkeypatch
):
    def fail_if_called(*args, **kwargs):
        raise AssertionError("QInputDialog.getItem should not be called for a single-sheet file")

    monkeypatch.setattr("benford_lens.ui.main_window.QInputDialog.getItem", fail_if_called)

    window.load_file(_write_single_sheet_excel(tmp_path))

    assert window.column_table.rowCount() == 2
    assert window.column_table.item(0, 0).text() == "name"
    assert window.column_table.item(1, 0).text() == "amount"


def test_load_file_multi_sheet_excel_prompts_and_loads_chosen_sheet(window, tmp_path, monkeypatch):
    def fake_get_item(parent, title, label, items, current, editable):
        assert items == ["Lookup", "Yearly"]
        return "Yearly", True

    monkeypatch.setattr("benford_lens.ui.main_window.QInputDialog.getItem", fake_get_item)

    window.load_file(_write_multi_sheet_excel_with_numeric_headers(tmp_path))

    assert window.column_table.rowCount() == 2
    assert window.column_table.item(0, 0).text() == "2021"
    assert window.column_table.item(1, 0).text() == "2022"
    assert window._columns == [2021, 2022]


def test_selecting_a_numeric_labeled_excel_column_enables_analyze_and_analyzes(
    window, tmp_path, monkeypatch
):
    # Regression test for Finding 1: str(2021) round-tripped through
    # QTableWidgetItem.text() is "2021", which is never equal to the int
    # column label 2021 pandas assigned from the numeric header cell. Before
    # the fix, selecting this row raised an unhandled ValueError inside the
    # itemSelectionChanged slot and Analyze silently stayed disabled.
    monkeypatch.setattr(
        "benford_lens.ui.main_window.QInputDialog.getItem",
        lambda *a, **k: ("Yearly", True),
    )

    window.load_file(_write_multi_sheet_excel_with_numeric_headers(tmp_path))
    window.column_table.selectRow(0)

    assert window.analyze_button.isEnabled() is True
    assert window.controller.state.selected_column == 2021

    window._on_analyze_clicked()

    assert window.canvas is not None
    result = window.controller.state.last_result
    assert result is not None
    assert result.sample_size == 3
    assert result.observed_counts[1] == 2
    assert result.observed_counts[2] == 1


def test_loading_a_new_file_clears_the_previous_chart(window, tmp_path):
    window.load_file(_write_csv(tmp_path))
    window.column_table.selectRow(1)
    window._on_analyze_clicked()
    assert window.canvas is not None

    window.load_file(_write_csv(tmp_path))

    assert window.canvas is None


def test_reselecting_a_column_clears_the_previous_chart(window, tmp_path):
    # Regression test: the previous chart's clickable digit bars belong to
    # the previously selected column. If the chart stayed live after
    # reselecting a different column, clicking it would call drill_down()
    # against the new column and silently return mismatched rows.
    window.load_file(_write_csv(tmp_path))
    window.column_table.selectRow(1)
    window._on_analyze_clicked()
    assert window.canvas is not None

    window.column_table.selectRow(0)

    assert window.canvas is None


def test_previewing_different_preprocessing_clears_the_previous_chart(window, tmp_path):
    # Regression test: the displayed chart was rendered under the
    # preprocessing options active at analyze() time. Previewing different
    # options updates the controller's current options, so a stale chart
    # click would call drill_down() against data that no longer matches
    # what's on screen unless the chart is cleared.
    window.load_file(_write_csv(tmp_path))
    window.column_table.selectRow(1)
    window._on_analyze_clicked()
    assert window.canvas is not None

    window.preprocessing_panel.preview_button.click()

    assert window.canvas is None


def test_selecting_a_column_enables_the_preprocessing_panel(window, tmp_path):
    window.load_file(_write_csv(tmp_path))

    assert window.preprocessing_panel.isEnabled() is False

    window.column_table.selectRow(1)

    assert window.preprocessing_panel.isEnabled() is True


def test_preprocessing_preview_button_shows_before_after_counts(window, tmp_path):
    window.load_file(_write_csv(tmp_path))
    window.column_table.selectRow(1)

    window.preprocessing_panel.preview_button.click()

    assert "3" in window.preprocessing_panel.result_label.text()


def test_analyze_uses_the_current_preprocessing_selection(window, tmp_path):
    path = tmp_path / "with_negative.csv"
    path.write_text("amount\n-111\n222\n0\n", encoding="utf-8")
    window.load_file(str(path))
    window.column_table.selectRow(0)
    window.preprocessing_panel.negative_combo.setCurrentIndex(
        window.preprocessing_panel.negative_combo.findData("exclude")
    )

    window._on_analyze_clicked()

    result = window.controller.state.last_result
    assert result is not None
    assert result.sample_size == 1


def test_selecting_a_column_shows_a_suitability_badge(window, tmp_path):
    window.load_file(_write_csv(tmp_path))

    window.column_table.selectRow(1)

    assert window.suitability_panel.badge_label.text() != ""


def test_clicking_a_digit_on_the_chart_shows_matching_rows(window, tmp_path):
    window.load_file(_write_csv(tmp_path))
    window.column_table.selectRow(1)
    window._on_analyze_clicked()

    window._on_chart_clicked(SimpleNamespace(xdata=1.2))

    assert window.drill_down_panel.table.rowCount() == 2  # alice=111, carol=111 both lead with 1


def test_clicking_outside_the_digit_range_does_nothing(window, tmp_path):
    window.load_file(_write_csv(tmp_path))
    window.column_table.selectRow(1)
    window._on_analyze_clicked()

    window._on_chart_clicked(SimpleNamespace(xdata=None))
    window._on_chart_clicked(SimpleNamespace(xdata=15))

    assert window.drill_down_panel.table.rowCount() == 0


def test_export_report_button_disabled_until_analyzed(window, tmp_path):
    window.load_file(_write_csv(tmp_path))
    window.column_table.selectRow(1)

    assert window.export_report_button.isEnabled() is False

    window._on_analyze_clicked()

    assert window.export_report_button.isEnabled() is True


def test_export_report_writes_an_html_file(window, tmp_path, monkeypatch):
    window.load_file(_write_csv(tmp_path))
    window.column_table.selectRow(1)
    window._on_analyze_clicked()

    out_path = tmp_path / "report.html"
    monkeypatch.setattr(
        "benford_lens.ui.main_window.QFileDialog.getSaveFileName",
        lambda *a, **k: (str(out_path), "HTML files (*.html)"),
    )

    window._on_export_report_clicked()

    assert out_path.exists()
    assert "amount" in out_path.read_text(encoding="utf-8")


def test_export_report_button_disabled_after_reselecting_a_column(window, tmp_path):
    window.load_file(_write_csv(tmp_path))
    window.column_table.selectRow(1)
    window._on_analyze_clicked()

    assert window.export_report_button.isEnabled() is True

    window.column_table.selectRow(0)

    assert window.export_report_button.isEnabled() is False


def test_export_report_button_disabled_after_previewing_preprocessing(window, tmp_path):
    window.load_file(_write_csv(tmp_path))
    window.column_table.selectRow(1)
    window._on_analyze_clicked()

    assert window.export_report_button.isEnabled() is True

    window.preprocessing_panel.preview_button.click()

    assert window.export_report_button.isEnabled() is False


def test_loading_a_new_file_clears_suitability_and_drill_down_panels(window, tmp_path):
    # Regression test: _populate_columns cleared the column table, the
    # buttons and the chart, but left the previous file's suitability badge
    # and drill-down rows on screen — and DrillDownPanel's Export CSV… would
    # have written the first file's rows while the second file was open.
    first = _write_csv(tmp_path)
    window.load_file(first)
    window.column_table.selectRow(1)
    window._on_analyze_clicked()
    window._on_chart_clicked(SimpleNamespace(xdata=1.2))

    assert window.suitability_panel.badge_label.text() != ""
    assert window.drill_down_panel.table.rowCount() > 0

    second = tmp_path / "other.csv"
    second.write_text("label,value\nx,9\ny,8\n", encoding="utf-8")
    window.load_file(str(second))

    assert window.suitability_panel.badge_label.text() == ""
    assert window.suitability_panel.notes_label.text() == ""
    assert window.drill_down_panel.table.rowCount() == 0
    assert window.drill_down_panel._rows is None


def test_reselecting_a_column_clears_the_drill_down_panel(window, tmp_path):
    # Regression test: the rows table was populated by a chart click against
    # the previously selected column, so it had to go with the chart.
    window.load_file(_write_csv(tmp_path))
    window.column_table.selectRow(1)
    window._on_analyze_clicked()
    window._on_chart_clicked(SimpleNamespace(xdata=1.2))

    assert window.drill_down_panel.table.rowCount() > 0

    window.column_table.selectRow(0)

    assert window.drill_down_panel.table.rowCount() == 0
    assert window.drill_down_panel._rows is None


def test_loading_a_new_file_resets_the_preprocessing_combos_to_defaults(window, tmp_path):
    # Regression test: SessionController resets state.preprocessing_options
    # for every new file, so a leftover combo selection made the suitability
    # badge describe options that were not the ones visibly selected.
    window.load_file(_write_csv(tmp_path))
    combo = window.preprocessing_panel.negative_combo
    combo.setCurrentIndex(combo.findData("exclude"))
    assert combo.currentData() == "exclude"

    second = tmp_path / "other.csv"
    second.write_text("label,value\nx,9\ny,8\n", encoding="utf-8")
    window.load_file(str(second))

    assert combo.currentData() == "absolute"
    assert window.preprocessing_panel.current_options() == PreprocessingOptions()


def test_changing_a_preprocessing_combo_without_preview_invalidates_the_analysis(window, tmp_path):
    # Regression test: only the Preview button and column reselection used to
    # invalidate analyzed state. Editing a combo directly left the old chart
    # on screen and the Export button enabled, so an exported report could
    # describe options the user never applied to the displayed result.
    window.load_file(_write_csv(tmp_path))
    window.column_table.selectRow(1)
    window._on_analyze_clicked()

    assert window.export_report_button.isEnabled() is True
    assert window.canvas is not None

    combo = window.preprocessing_panel.negative_combo
    combo.setCurrentIndex(combo.findData("exclude"))

    assert window.export_report_button.isEnabled() is False
    assert window.canvas is None


def test_export_report_describes_the_analysis_that_was_actually_run(window, tmp_path, monkeypatch):
    # Regression test: export used to re-run configure_preprocessing() against
    # the live panel, so the report's preprocessing section could claim
    # "3 → 0 values used" while its digit table showed 3 analyzed values.
    path = tmp_path / "negatives.csv"
    path.write_text("amount\n-111\n-222\n-333\n", encoding="utf-8")
    window.load_file(str(path))
    window.column_table.selectRow(0)
    window._on_analyze_clicked()  # default negative handling: absolute -> 3 values

    # Switch to options that would preprocess every value away, without
    # clicking Preview and without re-analyzing.
    combo = window.preprocessing_panel.negative_combo
    combo.setCurrentIndex(combo.findData("exclude"))

    out_path = tmp_path / "report.html"
    monkeypatch.setattr(
        "benford_lens.ui.main_window.QFileDialog.getSaveFileName",
        lambda *a, **k: (str(out_path), "HTML files (*.html)"),
    )
    window._on_export_report_clicked()

    html_text = out_path.read_text(encoding="utf-8")
    # Preprocessing section and digit table must agree: 3 values in, 3 used.
    assert "3 → 3 values used" in html_text
    assert "Negative values: absolute" in html_text
    assert "0 values used" not in html_text
    for digit in (1, 2, 3):
        assert f"<tr><td>{digit}</td><td>33.3%</td>" in html_text


def test_switching_language_translates_visible_strings(window):
    index = window.language_combo.findData("ko")
    window.language_combo.setCurrentIndex(index)

    assert window.open_button.text() != "Open File…"

    index_en = window.language_combo.findData("en")
    window.language_combo.setCurrentIndex(index_en)

    assert window.open_button.text() == "Open File…"


def test_switching_language_translates_drill_down_panel_strings(window):
    assert window.drill_down_panel.search_box.placeholderText() == "Search…"

    index = window.language_combo.findData("ko")
    window.language_combo.setCurrentIndex(index)

    assert window.drill_down_panel.search_box.placeholderText() != "Search…"

    index_en = window.language_combo.findData("en")
    window.language_combo.setCurrentIndex(index_en)

    assert window.drill_down_panel.search_box.placeholderText() == "Search…"


def test_switching_language_translates_preprocessing_combo_labels(window, tmp_path):
    window.load_file(_write_csv(tmp_path))
    window.column_table.selectRow(1)
    english_text = window.preprocessing_panel.negative_combo.itemText(
        window.preprocessing_panel.negative_combo.findData("absolute")
    )
    assert english_text == "Convert to absolute value"

    index = window.language_combo.findData("ko")
    window.language_combo.setCurrentIndex(index)

    translated_text = window.preprocessing_panel.negative_combo.itemText(
        window.preprocessing_panel.negative_combo.findData("absolute")
    )
    assert translated_text != english_text


def test_switching_language_translates_the_suitability_notes(window, tmp_path):
    # The notes are the most useful part of the suitability panel; before the
    # structured-note change they were built inside the Analysis Engine as
    # English prose, so they never passed through tr() and stayed English
    # while the surrounding chrome translated.
    window.load_file(_write_csv(tmp_path))
    window.column_table.selectRow(1)

    english_notes = window.suitability_panel.notes_label.text()
    assert "valid value" in english_notes

    window.language_combo.setCurrentIndex(window.language_combo.findData("ko"))

    translated_notes = window.suitability_panel.notes_label.text()
    assert translated_notes != english_notes
    assert "valid value" not in translated_notes
    assert "유효한 값" in translated_notes

    window.language_combo.setCurrentIndex(window.language_combo.findData("en"))

    assert window.suitability_panel.notes_label.text() == english_notes


def test_switching_language_translates_the_result_summary(window, tmp_path):
    window.load_file(_write_csv(tmp_path))
    window.column_table.selectRow(1)
    window._on_analyze_clicked()

    english_summary = window.summary_label.text()
    assert "too few" in english_summary.lower()

    window.language_combo.setCurrentIndex(window.language_combo.findData("ja"))

    translated_summary = window.summary_label.text()
    assert translated_summary != english_summary
    assert "ベンフォード" in translated_summary

    window.language_combo.setCurrentIndex(window.language_combo.findData("en"))

    assert window.summary_label.text() == english_summary


def test_switching_language_after_selecting_a_column_keeps_the_select_column_prompt(
    window, tmp_path
):
    # Regression test: _retranslate_ui unconditionally reset summary_label to
    # the "open a file" prompt whenever last_result was None, so switching
    # language after picking a column wrongly walked the user back a step.
    window.load_file(_write_csv(tmp_path))
    window.column_table.selectRow(1)
    assert window.summary_label.text() == "Select a column, then click Analyze."

    window.language_combo.setCurrentIndex(window.language_combo.findData("ko"))

    assert window.summary_label.text() == "열을 선택한 다음 분석을 클릭하세요."

    window.language_combo.setCurrentIndex(window.language_combo.findData("en"))

    assert window.summary_label.text() == "Select a column, then click Analyze."


def test_switching_language_before_opening_a_file_keeps_the_open_file_prompt(window):
    assert window.summary_label.text() == "Open a CSV or Excel file to begin."

    window.language_combo.setCurrentIndex(window.language_combo.findData("ko"))

    assert window.summary_label.text() == "시작하려면 CSV 또는 Excel 파일을 여세요."


def test_switching_language_translates_the_suitability_metric_labels(window, tmp_path):
    window.load_file(_write_csv(tmp_path))
    window.column_table.selectRow(1)
    panel = window.suitability_panel

    assert panel.metric_name_labels["sample_count"].text() == "Sample count"
    assert panel.metric_value_labels["sample_count"].text() == "3"

    window.language_combo.setCurrentIndex(window.language_combo.findData("ko"))

    assert panel.metric_name_labels["sample_count"].text() == "표본 개수"
    # The numbers themselves are unaffected by the language switch.
    assert panel.metric_value_labels["sample_count"].text() == "3"


def test_export_report_records_the_excel_sheet_that_was_analyzed(window, tmp_path, monkeypatch):
    monkeypatch.setattr(
        "benford_lens.ui.main_window.QInputDialog.getItem",
        lambda *a, **k: ("Yearly", True),
    )
    window.load_file(_write_multi_sheet_excel_with_numeric_headers(tmp_path))
    window.column_table.selectRow(0)
    window._on_analyze_clicked()

    out_path = tmp_path / "report.html"
    monkeypatch.setattr(
        "benford_lens.ui.main_window.QFileDialog.getSaveFileName",
        lambda *a, **k: (str(out_path), "HTML files (*.html)"),
    )
    window._on_export_report_clicked()

    assert "Sheet: Yearly" in out_path.read_text(encoding="utf-8")


def test_export_report_for_a_csv_has_no_sheet_fragment(window, tmp_path, monkeypatch):
    window.load_file(_write_csv(tmp_path))
    window.column_table.selectRow(1)
    window._on_analyze_clicked()

    out_path = tmp_path / "report.html"
    monkeypatch.setattr(
        "benford_lens.ui.main_window.QFileDialog.getSaveFileName",
        lambda *a, **k: (str(out_path), "HTML files (*.html)"),
    )
    window._on_export_report_clicked()

    html_text = out_path.read_text(encoding="utf-8")
    assert "Sheet:" not in html_text
    assert "Source: data.csv — Column: amount" in html_text


def test_switching_language_after_opening_a_file_keeps_the_select_column_prompt(window, tmp_path):
    # _populate_columns shows the "select a column" prompt as soon as a file
    # is open, before any column is picked — retranslating must not walk that
    # back to the "open a file" prompt either.
    window.load_file(_write_csv(tmp_path))
    assert window.controller.state.selected_column is None
    assert window.summary_label.text() == "Select a column, then click Analyze."

    window.language_combo.setCurrentIndex(window.language_combo.findData("ko"))

    assert window.summary_label.text() == "열을 선택한 다음 분석을 클릭하세요."
