"""Collapsed expert-statistics panel for one analysis snapshot."""

from __future__ import annotations

from PySide6.QtWidgets import QFormLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from benford_lens.analysis.expert_statistics import ExpertStatistics

_STATISTIC_KEYS = (
    "sample_size",
    "mean_absolute_deviation",
    "chi_square_statistic",
    "chi_square_p_value",
    "ks_statistic",
    "ks_p_value",
)
_EMPTY_VALUE = "—"


def _format_statistic(key: str, value: int | float | None) -> str:
    if value is None:
        return _EMPTY_VALUE
    if key == "sample_size":
        return f"{int(value):,}"
    numeric_value = float(value)
    if numeric_value != 0 and abs(numeric_value) < 0.0001:
        return f"{numeric_value:.3e}"
    return f"{numeric_value:.6f}"


class ExpertStatisticsPanel(QWidget):
    """Show reference statistics on demand; details start collapsed."""

    def __init__(self) -> None:
        super().__init__()
        self._statistics: ExpertStatistics | None = None

        self.toggle_button = QPushButton(self.tr("Show Details"))
        self.toggle_button.setCheckable(True)
        self.toggle_button.setEnabled(False)
        self.toggle_button.toggled.connect(self._on_toggled)

        self.name_labels: dict[str, QLabel] = {}
        self.value_labels: dict[str, QLabel] = {}
        form = QFormLayout()
        for key in _STATISTIC_KEYS:
            name_label = QLabel("")
            value_label = QLabel("")
            self.name_labels[key] = name_label
            self.value_labels[key] = value_label
            form.addRow(name_label, value_label)

        self.caption_label = QLabel(self._caption_text())
        self.caption_label.setWordWrap(True)

        details_layout = QVBoxLayout()
        details_layout.addLayout(form)
        details_layout.addWidget(self.caption_label)
        self.details_widget = QWidget()
        self.details_widget.setLayout(details_layout)
        self.details_widget.setVisible(False)

        layout = QVBoxLayout()
        layout.addWidget(self.toggle_button)
        layout.addWidget(self.details_widget)
        self.setLayout(layout)
        self._retranslate_names()

    def _name_texts(self) -> dict[str, str]:
        return {
            "sample_size": self.tr("Sample size"),
            "mean_absolute_deviation": self.tr("Mean absolute deviation (MAD)"),
            "chi_square_statistic": self.tr("Chi-square statistic"),
            "chi_square_p_value": self.tr("Chi-square p-value"),
            "ks_statistic": self.tr("KS statistic"),
            "ks_p_value": self.tr("KS p-value"),
        }

    def _retranslate_names(self) -> None:
        for key, text in self._name_texts().items():
            self.name_labels[key].setText(text)

    def _caption_text(self) -> str:
        return self.tr(
            "Reference statistics only. Interpret them in light of the data and sample "
            "characteristics. KS compares base-10 log mantissas with a uniform distribution."
        )

    def _toggle_text(self) -> str:
        if self.toggle_button.isChecked():
            return self.tr("Hide Details")
        return self.tr("Show Details")

    def _on_toggled(self, checked: bool) -> None:
        self.details_widget.setVisible(checked)
        self.toggle_button.setText(self._toggle_text())

    def show_statistics(self, statistics: ExpertStatistics) -> None:
        self._statistics = statistics
        for key in _STATISTIC_KEYS:
            self.value_labels[key].setText(_format_statistic(key, getattr(statistics, key)))
        self.toggle_button.setEnabled(True)

    def clear(self) -> None:
        """Drop values and restore the default collapsed state."""
        self._statistics = None
        self.toggle_button.setChecked(False)
        self.toggle_button.setEnabled(False)
        self.details_widget.setVisible(False)
        for value_label in self.value_labels.values():
            value_label.setText("")

    def retranslate_ui(self) -> None:
        self._retranslate_names()
        self.caption_label.setText(self._caption_text())
        self.toggle_button.setText(self._toggle_text())
