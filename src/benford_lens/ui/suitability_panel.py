"""Suitability panel: an advisory 🟢/🟡/🔴 signal plus the underlying notes.

Never states or implies whether Benford's Law applies to the data; it presents
characteristics for the user to review.
"""

from __future__ import annotations

from PySide6.QtWidgets import QFormLayout, QLabel, QVBoxLayout, QWidget

from benford_lens.analysis.suitability import (
    NOTE_HIGH_MISSING_RATE,
    NOTE_HIGH_NEGATIVE_RATE,
    NOTE_HIGH_ZERO_RATE,
    NOTE_LOW_DIVERSITY,
    NOTE_NARROW_MAGNITUDE_RANGE,
    NOTE_REPEATED_VALUES,
    NOTE_SAMPLE_MODEST,
    NOTE_SAMPLE_TOO_SMALL,
    NOTE_SINGLE_MAGNITUDE,
    SuitabilityAssessment,
    SuitabilityLevel,
    SuitabilityMetrics,
    SuitabilityNote,
)

# SuitabilityMetrics fields, in the order they are shown to the user.
_METRIC_KEYS = (
    "sample_count",
    "min_value",
    "max_value",
    "digit_range",
    "distinct_value_count",
    "duplicate_rate",
    "zero_rate",
    "negative_rate",
    "missing_rate",
)
_RATE_KEYS = frozenset({"duplicate_rate", "zero_rate", "negative_rate", "missing_rate"})
_EMPTY_VALUE = "—"


def _format_metric(key: str, value: float | None) -> str:
    if value is None:
        return _EMPTY_VALUE
    if key in _RATE_KEYS:
        return f"{value:.1%}"
    if key in ("min_value", "max_value"):
        return f"{value:,.1f}"
    return f"{int(value):,}"


class SuitabilityPanel(QWidget):
    def __init__(self) -> None:
        super().__init__()
        # Kept so a language switch can re-render the badge and notes; they
        # are built from translated templates, not stored as finished text.
        self._assessment: SuitabilityAssessment | None = None
        self.badge_label = QLabel("")
        self.notes_label = QLabel("")
        self.notes_label.setWordWrap(True)
        self.caption_label = QLabel(self._caption_text())
        self.caption_label.setWordWrap(True)

        self.metric_name_labels: dict[str, QLabel] = {}
        self.metric_value_labels: dict[str, QLabel] = {}
        metrics_form = QFormLayout()
        for key in _METRIC_KEYS:
            name_label = QLabel("")
            value_label = QLabel("")
            self.metric_name_labels[key] = name_label
            self.metric_value_labels[key] = value_label
            metrics_form.addRow(name_label, value_label)
        self._retranslate_metric_names()

        layout = QVBoxLayout()
        layout.addWidget(self.badge_label)
        layout.addWidget(self.notes_label)
        layout.addLayout(metrics_form)
        layout.addWidget(self.caption_label)
        self.setLayout(layout)

    def _metric_name_texts(self) -> dict[str, str]:
        """Row label per SuitabilityMetrics field.

        Plain descriptive names: these report what the data looks like, they
        do not characterise it.
        """
        return {
            "sample_count": self.tr("Sample count"),
            "min_value": self.tr("Minimum value"),
            "max_value": self.tr("Maximum value"),
            "digit_range": self.tr("Magnitude range"),
            "distinct_value_count": self.tr("Distinct values"),
            "duplicate_rate": self.tr("Duplicate rate"),
            "zero_rate": self.tr("Zero rate"),
            "negative_rate": self.tr("Negative rate"),
            "missing_rate": self.tr("Missing rate"),
        }

    def _retranslate_metric_names(self) -> None:
        for key, text in self._metric_name_texts().items():
            self.metric_name_labels[key].setText(text)

    def _show_metrics(self, metrics: SuitabilityMetrics) -> None:
        for key in _METRIC_KEYS:
            self.metric_value_labels[key].setText(_format_metric(key, getattr(metrics, key)))

    def _caption_text(self) -> str:
        return self.tr(
            "These are data characteristics, not a determination of whether Benford's Law "
            "applies — that judgment is yours to make."
        )

    def _badge_text(self, level: SuitabilityLevel) -> str:
        if level is SuitabilityLevel.GOOD:
            return self.tr("\U0001f7e2 Good")
        if level is SuitabilityLevel.CAUTION:
            return self.tr("\U0001f7e1 Caution")
        return self.tr("\U0001f534 Difficult to determine")

    def _note_templates(self) -> dict[str, str]:
        """Translatable template per advisory-note code.

        Wording is neutral and exploratory: these describe data characteristics
        only, never a verdict about the data.
        """
        return {
            NOTE_SAMPLE_TOO_SMALL: self.tr(
                "Only {sample_count} valid value(s) — below the {minimum}-value floor "
                "for a meaningful comparison."
            ),
            NOTE_SAMPLE_MODEST: self.tr(
                "{sample_count} valid values is a workable but modest sample size."
            ),
            NOTE_SINGLE_MAGNITUDE: self.tr("Values span only a single order of magnitude."),
            NOTE_NARROW_MAGNITUDE_RANGE: self.tr("Values span {digit_range} orders of magnitude."),
            NOTE_LOW_DIVERSITY: self.tr("Very few distinct values relative to the sample size."),
            NOTE_REPEATED_VALUES: self.tr(
                "Values repeat somewhat more than expected for this sample size."
            ),
            NOTE_HIGH_ZERO_RATE: self.tr("{zero_rate:.0%} of the source values were zero."),
            NOTE_HIGH_NEGATIVE_RATE: self.tr(
                "{negative_rate:.0%} of the source values were negative — check whether the "
                "negative-value preprocessing option fits this data."
            ),
            NOTE_HIGH_MISSING_RATE: self.tr("{missing_rate:.0%} of the source values were blank."),
        }

    def note_text(self, note: SuitabilityNote) -> str:
        template = self._note_templates().get(note.code)
        if template is None:  # pragma: no cover - defensive, every code is mapped
            return note.code
        return template.format(**note.params)

    def show_assessment(self, assessment: SuitabilityAssessment) -> None:
        self._assessment = assessment
        self.badge_label.setText(self._badge_text(assessment.level))
        notes_text = "\n".join(f"• {self.note_text(note)}" for note in assessment.notes)
        self.notes_label.setText(notes_text or self.tr("No caveats found."))
        self._show_metrics(assessment.metrics)

    def clear(self) -> None:
        """Blank the badge, notes and metrics.

        Called when a new file is loaded: the previous file's badge would
        otherwise stay on screen describing data that is no longer open.
        """
        self._assessment = None
        self.badge_label.setText("")
        self.notes_label.setText("")
        for value_label in self.metric_value_labels.values():
            value_label.setText("")

    def retranslate_ui(self) -> None:
        self.caption_label.setText(self._caption_text())
        self._retranslate_metric_names()
        if self._assessment is not None:
            self.show_assessment(self._assessment)
