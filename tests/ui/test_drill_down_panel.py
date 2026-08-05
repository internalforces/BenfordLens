import pandas as pd
import pytest
from PySide6.QtWidgets import QApplication

from benford_lens.ui.drill_down_panel import DrillDownPanel


@pytest.fixture
def app():
    application = QApplication.instance() or QApplication([])
    yield application


@pytest.fixture
def panel(app):
    widget = DrillDownPanel()
    yield widget
    widget.close()


def _rows() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "name": ["Acme (Holdings)", "Beta [Group]", "Gamma * Co", "Delta + Sons", "Eps?ilon"],
            "amount": [111, 122, 133, 144, 155],
        }
    )


def test_show_rows_renders_every_row(panel):
    panel.show_rows(_rows())

    assert panel.table.rowCount() == 5
    assert panel.table.columnCount() == 2


def test_search_filters_by_plain_substring(panel):
    panel.show_rows(_rows())

    panel.search_box.setText("beta")  # case-insensitive substring

    assert panel.table.rowCount() == 1
    assert panel.table.item(0, 0).text() == "Beta [Group]"


@pytest.mark.parametrize(
    ("needle", "expected"),
    [
        ("(", "Acme (Holdings)"),
        ("[", "Beta [Group]"),
        ("*", "Gamma * Co"),
        ("+", "Delta + Sons"),
        ("?", "Eps?ilon"),
    ],
)
def test_search_handles_regex_metacharacters_as_literal_text(panel, needle, expected):
    # Regression test: pandas' .str.contains defaults to regex=True, so these
    # characters raised re.error inside the textChanged slot instead of
    # matching literally. The spec asks for plain substring search.
    panel.show_rows(_rows())

    panel.search_box.setText(needle)

    assert panel.table.rowCount() == 1
    assert panel.table.item(0, 0).text() == expected


def test_search_matching_nothing_empties_the_table(panel):
    panel.show_rows(_rows())

    panel.search_box.setText("no-such-value")

    assert panel.table.rowCount() == 0


def test_show_rows_renders_once_when_a_previous_search_was_active(panel, monkeypatch):
    # Regression test: show_rows set self._rows before clearing the search
    # box, so clear() fired textChanged -> _apply_filter -> a render, which
    # show_rows then immediately threw away with its own _render call.
    panel.show_rows(_rows())
    panel.search_box.setText("beta")

    render_calls = []
    original_render = panel._render
    monkeypatch.setattr(
        panel, "_render", lambda rows: (render_calls.append(len(rows)), original_render(rows))[1]
    )

    panel.show_rows(_rows())

    assert render_calls == [5]
    assert panel.search_box.text() == ""
    assert panel.table.rowCount() == 5


def test_clear_empties_the_table_and_drops_the_rows(panel):
    # Regression test: without clear(), a stale Export CSV click would write
    # the previous file's rows while a different file is open.
    panel.show_rows(_rows())

    panel.clear()

    assert panel.table.rowCount() == 0
    assert panel.table.columnCount() == 0
    assert panel._rows is None
    assert panel.search_box.text() == ""
