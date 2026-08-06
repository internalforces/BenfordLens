import pytest
from PySide6.QtWidgets import QApplication

from benford_lens.analysis.expert_statistics import ExpertStatistics
from benford_lens.ui.expert_statistics_panel import ExpertStatisticsPanel


@pytest.fixture
def app():
    application = QApplication.instance() or QApplication([])
    yield application


@pytest.fixture
def panel(app):
    widget = ExpertStatisticsPanel()
    yield widget
    widget.close()


def _statistics() -> ExpertStatistics:
    return ExpertStatistics(
        sample_size=1234,
        mean_absolute_deviation=0.0123456,
        chi_square_statistic=17.25,
        chi_square_p_value=0.0275,
        ks_statistic=0.09876,
        ks_p_value=0.0000123,
    )


def test_details_are_collapsed_and_disabled_before_analysis(panel):
    assert panel.details_widget.isHidden() is True
    assert panel.toggle_button.isEnabled() is False
    assert panel.toggle_button.isChecked() is False


def test_show_statistics_populates_values_without_expanding_details(panel):
    panel.show_statistics(_statistics())

    assert panel.toggle_button.isEnabled() is True
    assert panel.details_widget.isHidden() is True
    assert panel.value_labels["sample_size"].text() == "1,234"
    assert panel.value_labels["mean_absolute_deviation"].text() == "0.012346"
    assert panel.value_labels["chi_square_statistic"].text() == "17.250000"
    assert panel.value_labels["chi_square_p_value"].text() == "0.027500"
    assert panel.value_labels["ks_statistic"].text() == "0.098760"
    assert panel.value_labels["ks_p_value"].text() == "1.230e-05"


def test_toggle_reveals_and_hides_details(panel):
    panel.show_statistics(_statistics())

    panel.toggle_button.setChecked(True)
    assert panel.details_widget.isHidden() is False
    assert panel.toggle_button.text() == "Hide Details"

    panel.toggle_button.setChecked(False)
    assert panel.details_widget.isHidden() is True
    assert panel.toggle_button.text() == "Show Details"


def test_clear_removes_values_and_restores_collapsed_default(panel):
    panel.show_statistics(_statistics())
    panel.toggle_button.setChecked(True)

    panel.clear()

    assert panel.toggle_button.isEnabled() is False
    assert panel.toggle_button.isChecked() is False
    assert panel.details_widget.isHidden() is True
    assert all(label.text() == "" for label in panel.value_labels.values())


def test_undefined_statistics_use_a_placeholder(panel):
    panel.show_statistics(
        ExpertStatistics(
            sample_size=0,
            mean_absolute_deviation=None,
            chi_square_statistic=None,
            chi_square_p_value=None,
            ks_statistic=None,
            ks_p_value=None,
        )
    )

    assert panel.value_labels["sample_size"].text() == "0"
    assert panel.value_labels["mean_absolute_deviation"].text() == "—"
    assert panel.value_labels["ks_p_value"].text() == "—"
