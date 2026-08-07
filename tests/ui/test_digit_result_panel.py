from types import SimpleNamespace

import pytest
from PySide6.QtWidgets import QApplication

from benford_lens.analysis.benford import DigitPosition, analyze_second_digit
from benford_lens.ui.digit_result_panel import DigitResultPanel


class _WheelEventStub:
    def __init__(self) -> None:
        self.ignored = False

    def ignore(self) -> None:
        self.ignored = True


@pytest.fixture
def app():
    application = QApplication.instance() or QApplication([])
    yield application


@pytest.fixture
def panel(app):
    widget = DigitResultPanel(DigitPosition.SECOND)
    yield widget
    widget.close()


def test_show_result_renders_second_digit_chart_and_summary(panel):
    panel.show_result(
        analyze_second_digit([101, 111, 222, 5]),
        title="Second digit",
        summary="Summary",
        x_axis_label="Second digit",
        y_axis_label="Proportion (%)",
        observed_label="Observed",
        expected_label="Expected",
    )

    assert panel.canvas is not None
    assert panel.title_label.text() == "Second digit"
    assert panel.summary_label.text() == "Summary"
    assert list(panel.canvas.figure.axes[0].get_xticks()) == list(range(10))


def test_chart_click_emits_position_and_valid_digit(panel):
    clicks = []
    panel.digit_clicked.connect(lambda position, digit: clicks.append((position, digit)))
    panel.show_result(
        analyze_second_digit([101, 111]),
        title="Second digit",
        summary="Summary",
        x_axis_label="Second digit",
        y_axis_label="Proportion (%)",
        observed_label="Observed",
        expected_label="Expected",
    )

    panel._on_chart_clicked(SimpleNamespace(xdata=0.2))
    panel._on_chart_clicked(SimpleNamespace(xdata=15))
    panel._on_chart_clicked(SimpleNamespace(xdata=None))

    assert clicks == [(DigitPosition.SECOND, 0)]


def test_chart_wheel_event_is_left_for_the_parent_scroll_area(panel):
    panel.show_result(
        analyze_second_digit([101, 111]),
        title="Second digit",
        summary="Summary",
        x_axis_label="Second digit",
        y_axis_label="Proportion (%)",
        observed_label="Observed",
        expected_label="Expected",
    )
    event = _WheelEventStub()

    assert panel.canvas is not None
    panel.canvas.wheelEvent(event)  # type: ignore[arg-type]

    assert event.ignored is True


def test_clear_removes_chart_and_text(panel):
    panel.show_result(
        analyze_second_digit([101]),
        title="Second digit",
        summary="Summary",
        x_axis_label="Second digit",
        y_axis_label="Proportion (%)",
        observed_label="Observed",
        expected_label="Expected",
    )

    panel.clear()

    assert panel.canvas is None
    assert panel.result is None
    assert panel.title_label.text() == ""
    assert panel.summary_label.text() == ""
