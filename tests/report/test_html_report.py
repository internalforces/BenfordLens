from matplotlib.figure import Figure

from benford_lens.analysis.benford import BenfordResult
from benford_lens.analysis.preprocessing import PreprocessingOptions, PreprocessingPreview
from benford_lens.analysis.suitability import (
    NOTE_NARROW_MAGNITUDE_RANGE,
    SuitabilityAssessment,
    SuitabilityLevel,
    SuitabilityMetrics,
    SuitabilityNote,
)
from benford_lens.charts.benford_chart import SUMMARY_CLOSE_TO_BENFORD, ResultSummary
from benford_lens.report.html_report import ReportContext, render_html_report


def _build_context() -> ReportContext:
    result = BenfordResult(
        observed_counts={d: 1 for d in range(1, 10)},
        observed_proportions={d: 1 / 9 for d in range(1, 10)},
        expected_proportions={d: 1 / 9 for d in range(1, 10)},
        sample_size=9,
    )
    preview = PreprocessingPreview(
        total_before=10,
        total_after=9,
        excluded_negative=0,
        excluded_zero=1,
        excluded_blank=0,
        excluded_non_numeric=0,
        sample_before=[1, 2, 3],
        sample_after=[1.0, 2.0, 3.0],
    )
    metrics = SuitabilityMetrics(
        sample_count=9,
        min_value=1.0,
        max_value=900.0,
        digit_range=3,
        duplicate_rate=0.0,
        zero_rate=0.1,
        negative_rate=0.0,
        missing_rate=0.0,
        distinct_value_count=9,
    )
    assessment = SuitabilityAssessment(
        level=SuitabilityLevel.CAUTION,
        metrics=metrics,
        notes=[SuitabilityNote(NOTE_NARROW_MAGNITUDE_RANGE, {"digit_range": 3})],
    )
    figure = Figure()
    figure.add_subplot(111).bar([1, 2], [10, 20])

    return ReportContext(
        source_name="sample.csv",
        column_name="amount",
        preprocessing_options=PreprocessingOptions(),
        preprocessing_preview=preview,
        suitability=assessment,
        result=result,
        result_summary=ResultSummary(SUMMARY_CLOSE_TO_BENFORD),
        chart_figure=figure,
    )


def test_render_html_report_includes_key_content():
    html = render_html_report(_build_context())

    assert "sample.csv" in html
    assert "amount" in html
    assert "Caution" in html
    assert "Values span 3 orders of magnitude." in html
    assert "data:image/png;base64," in html
    assert "close to the expected Benford distribution" in html
    assert "no data was sent anywhere" in html.lower()


def test_render_html_report_never_uses_accusatory_wording():
    html = render_html_report(_build_context()).lower()

    assert "fraudulent" not in html
    assert " fraud " not in html
    assert "manipulated" not in html


def test_render_html_report_escapes_user_derived_strings():
    """Regression test: verify HTML special chars in user input are escaped, not injected."""
    result = BenfordResult(
        observed_counts={d: 1 for d in range(1, 10)},
        observed_proportions={d: 1 / 9 for d in range(1, 10)},
        expected_proportions={d: 1 / 9 for d in range(1, 10)},
        sample_size=9,
    )
    preview = PreprocessingPreview(
        total_before=10,
        total_after=9,
        excluded_negative=0,
        excluded_zero=1,
        excluded_blank=0,
        excluded_non_numeric=0,
        sample_before=[1, 2, 3],
        sample_after=[1.0, 2.0, 3.0],
    )
    metrics = SuitabilityMetrics(
        sample_count=9,
        min_value=1.0,
        max_value=900.0,
        digit_range=3,
        duplicate_rate=0.0,
        zero_rate=0.1,
        negative_rate=0.0,
        missing_rate=0.0,
        distinct_value_count=9,
    )
    assessment = SuitabilityAssessment(
        level=SuitabilityLevel.CAUTION,
        metrics=metrics,
        notes=[SuitabilityNote(NOTE_NARROW_MAGNITUDE_RANGE, {"digit_range": 3})],
    )
    figure = Figure()
    figure.add_subplot(111).bar([1, 2], [10, 20])

    # Create context with malicious HTML in every user-derived field. (The
    # notes and the result summary are no longer user-derived: they are
    # rendered from fixed templates keyed by a code, with numeric params.)
    context = ReportContext(
        source_name="</p><script>alert(1)</script><p>evil.csv",
        column_name="Price < Discount & <b>weird</b>",
        preprocessing_options=PreprocessingOptions(),
        preprocessing_preview=preview,
        suitability=assessment,
        result=result,
        result_summary=ResultSummary(SUMMARY_CLOSE_TO_BENFORD),
        chart_figure=figure,
    )

    html = render_html_report(context)

    # Verify raw HTML tags are NOT present in the output (unescaped)
    assert "<script>" not in html
    assert "</p><script>" not in html

    # Verify escaped forms ARE present (source_name, column_name)
    assert "&lt;script&gt;" in html
    assert "&lt;b&gt;" in html
    assert "Price &lt; Discount" in html
