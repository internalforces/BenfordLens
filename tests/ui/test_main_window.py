import pytest
from PySide6.QtWidgets import QApplication

from benford_lens.ui.main_window import MainWindow


@pytest.fixture
def app():
    application = QApplication.instance() or QApplication([])
    yield application


@pytest.fixture
def window(app):
    win = MainWindow()
    yield win
    win.close()


def _write_csv(tmp_path):
    path = tmp_path / "data.csv"
    path.write_text("name,amount\nalice,111\nbob,222\ncarol,111\n", encoding="utf-8")
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


def test_load_file_shows_error_dialog_on_bad_path(window, tmp_path, monkeypatch):
    shown = {}

    def fake_critical(parent, title, text):
        shown["title"] = title
        shown["text"] = text

    monkeypatch.setattr(
        "benford_lens.ui.main_window.QMessageBox.critical", fake_critical
    )

    window.load_file(str(tmp_path / "missing.csv"))

    assert shown["title"] == "Could not open file"
    assert window.column_table.rowCount() == 0
