"""The exported report is English-only; the UI is translated.

Both render the same structured codes, from two separate template tables
(the UI's must be `tr()` literals so `pyside6-lupdate` can extract them).
These tests keep the two tables from drifting apart and hold every template
to the project's neutral, exploratory wording boundary.
"""

import pytest
from PySide6.QtWidgets import QApplication

from benford_lens.analysis.suitability import SuitabilityNote
from benford_lens.charts.benford_chart import ResultSummary
from benford_lens.report.html_report import (
    RESULT_SUMMARY_TEMPLATES,
    SUITABILITY_NOTE_TEMPLATES,
    format_result_summary,
    format_suitability_note,
)
from benford_lens.ui.main_window import MainWindow
from benford_lens.ui.suitability_panel import SuitabilityPanel

# One representative parameter set per code, covering every branch
# assess_suitability()/summarize_result() can emit.
NOTE_PARAMS: dict[str, dict[str, object]] = {
    "SAMPLE_TOO_SMALL": {"sample_count": 10, "minimum": 30},
    "SAMPLE_MODEST": {"sample_count": 100},
    "SINGLE_MAGNITUDE": {},
    "NARROW_MAGNITUDE_RANGE": {"digit_range": 3},
    "LOW_DIVERSITY": {},
    "REPEATED_VALUES": {},
    "HIGH_ZERO_RATE": {"zero_rate": 0.4},
    "HIGH_NEGATIVE_RATE": {"negative_rate": 0.66},
    "HIGH_MISSING_RATE": {"missing_rate": 0.35},
}

SUMMARY_PARAMS: dict[str, dict[str, object]] = {
    "NO_VALID_VALUES": {},
    "SAMPLE_TOO_SMALL": {"sample_size": 3},
    "CLOSE_TO_BENFORD": {},
    "DIVERGES_FROM_BENFORD": {},
}

RESTRICTED_FRAGMENTS = (
    "fr" + "aud",
    "fr" + "audulent",
    "manip" + "ulated",
    "manip" + "ulation",
)


@pytest.fixture
def app():
    application = QApplication.instance() or QApplication([])
    yield application


def test_every_note_code_has_params_coverage():
    assert set(NOTE_PARAMS) == set(SUITABILITY_NOTE_TEMPLATES)


def test_every_summary_code_has_params_coverage():
    assert set(SUMMARY_PARAMS) == set(RESULT_SUMMARY_TEMPLATES)


@pytest.mark.parametrize("code", sorted(NOTE_PARAMS))
def test_note_renders_identically_in_the_report_and_the_untranslated_ui(app, code):
    panel = SuitabilityPanel()
    try:
        note = SuitabilityNote(code, NOTE_PARAMS[code])
        assert panel.note_text(note) == format_suitability_note(note)
    finally:
        panel.close()


@pytest.mark.parametrize("code", sorted(SUMMARY_PARAMS))
def test_summary_renders_identically_in_the_report_and_the_untranslated_ui(app, code):
    window = MainWindow()
    try:
        summary = ResultSummary(code, SUMMARY_PARAMS[code])
        assert window._summary_text(summary) == format_result_summary(summary)
    finally:
        window.close()


@pytest.mark.parametrize("code", sorted(NOTE_PARAMS))
def test_note_wording_is_neutral(code):
    text = format_suitability_note(SuitabilityNote(code, NOTE_PARAMS[code])).lower()

    for restricted in RESTRICTED_FRAGMENTS:
        assert restricted not in text


@pytest.mark.parametrize("code", sorted(SUMMARY_PARAMS))
def test_summary_wording_is_neutral(code):
    text = format_result_summary(ResultSummary(code, SUMMARY_PARAMS[code])).lower()

    for restricted in RESTRICTED_FRAGMENTS:
        assert restricted not in text
