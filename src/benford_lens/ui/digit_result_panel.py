"""Reusable chart-and-summary panel for one significant-digit position."""

from __future__ import annotations

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QLabel, QSizePolicy, QVBoxLayout, QWidget

from benford_lens.analysis.benford import BenfordResult, DigitPosition
from benford_lens.charts.benford_chart import build_digit_figure


class DigitResultPanel(QWidget):
    """Render one digit distribution and emit validated chart clicks."""

    digit_clicked = Signal(object, int)

    def __init__(self, position: DigitPosition) -> None:
        super().__init__()
        self.position = position
        self.result: BenfordResult | None = None
        self.canvas: FigureCanvasQTAgg | None = None

        self.title_label = QLabel("")
        self.summary_label = QLabel("")
        self.summary_label.setWordWrap(True)
        self.chart_layout = QVBoxLayout()

        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.summary_label)
        layout.addLayout(self.chart_layout)
        self.setLayout(layout)

    def show_result(
        self,
        result: BenfordResult,
        *,
        title: str,
        summary: str,
        x_axis_label: str,
        y_axis_label: str,
        observed_label: str,
        expected_label: str,
    ) -> None:
        """Render a result with presentation strings supplied by the window."""
        self.clear_chart()
        self.result = result
        self.title_label.setText(title)
        self.summary_label.setText(summary)
        figure = build_digit_figure(
            result,
            x_axis_label=x_axis_label,
            y_axis_label=y_axis_label,
            observed_label=observed_label,
            expected_label=expected_label,
        )
        self.canvas = FigureCanvasQTAgg(figure)
        self.canvas.setMinimumHeight(300)
        self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.canvas.mpl_connect("button_press_event", self._on_chart_clicked)
        self.chart_layout.addWidget(self.canvas)

    def set_prompt(self, text: str) -> None:
        """Show workflow guidance while no result is active."""
        self.clear_chart()
        self.result = None
        self.title_label.setText("")
        self.summary_label.setText(text)

    def clear_chart(self) -> None:
        """Remove the current chart without changing panel visibility."""
        if self.canvas is not None:
            self.chart_layout.removeWidget(self.canvas)
            self.canvas.deleteLater()
            self.canvas = None

    def clear(self) -> None:
        """Remove all result content."""
        self.clear_chart()
        self.result = None
        self.title_label.setText("")
        self.summary_label.setText("")

    def _on_chart_clicked(self, event) -> None:
        if self.result is None or event.xdata is None:
            return
        digit = round(event.xdata)
        if digit not in self.result.expected_proportions:
            return
        self.digit_clicked.emit(self.position, int(digit))
