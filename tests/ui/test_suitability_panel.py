import pytest
from PySide6.QtWidgets import QApplication

from benford_lens.analysis.suitability import (
    NOTE_NARROW_MAGNITUDE_RANGE,
    SuitabilityAssessment,
    SuitabilityLevel,
    SuitabilityMetrics,
    SuitabilityNote,
)
from benford_lens.ui.suitability_panel import SuitabilityPanel


@pytest.fixture
def app():
    application = QApplication.instance() or QApplication([])
    yield application


@pytest.fixture
def panel(app):
    widget = SuitabilityPanel()
    yield widget
    widget.close()


def _assessment(**overrides) -> SuitabilityAssessment:
    metrics = SuitabilityMetrics(
        sample_count=1234,
        min_value=12.5,
        max_value=987654.0,
        digit_range=6,
        duplicate_rate=0.125,
        zero_rate=0.04,
        negative_rate=0.5,
        missing_rate=0.0,
        distinct_value_count=1080,
    )
    for key, value in overrides.items():
        setattr(metrics, key, value)
    return SuitabilityAssessment(
        level=SuitabilityLevel.CAUTION,
        metrics=metrics,
        notes=[SuitabilityNote(NOTE_NARROW_MAGNITUDE_RANGE, {"digit_range": 6})],
    )


def test_show_assessment_displays_every_metric(panel):
    # Regression test: the panel computed all nine SuitabilityMetrics fields
    # but showed the user none of them — only the badge, notes and caption.
    panel.show_assessment(_assessment())

    values = {key: label.text() for key, label in panel.metric_value_labels.items()}

    assert values["sample_count"] == "1,234"
    assert values["min_value"] == "12.5"
    assert values["max_value"] == "987,654.0"
    assert values["digit_range"] == "6"
    assert values["distinct_value_count"] == "1,080"
    assert values["duplicate_rate"] == "12.5%"
    assert values["zero_rate"] == "4.0%"
    assert values["negative_rate"] == "50.0%"
    assert values["missing_rate"] == "0.0%"


def test_every_metric_row_has_a_visible_name(panel):
    panel.show_assessment(_assessment())

    for key, label in panel.metric_name_labels.items():
        assert label.text() != "", key


def test_missing_min_and_max_render_as_a_placeholder(panel):
    panel.show_assessment(_assessment(sample_count=0, min_value=None, max_value=None))

    assert panel.metric_value_labels["min_value"].text() == "—"
    assert panel.metric_value_labels["max_value"].text() == "—"
    assert panel.metric_value_labels["sample_count"].text() == "0"


def test_clear_blanks_the_metrics(panel):
    panel.show_assessment(_assessment())

    panel.clear()

    for key, label in panel.metric_value_labels.items():
        assert label.text() == "", key
