from matplotlib.figure import Figure

from benford_lens.analysis.benford import BenfordResult
from benford_lens.analysis.preprocessing import PreprocessingOptions, PreprocessingPreview
from benford_lens.analysis.suitability import (
    SuitabilityAssessment,
    SuitabilityLevel,
    SuitabilityMetrics,
)
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
        notes=["Values span 3 orders of magnitude."],
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
        result_summary="The overall distribution is close to the expected Benford distribution.",
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
        notes=["<script>alert(1)</script>"],
    )
    figure = Figure()
    figure.add_subplot(111).bar([1, 2], [10, 20])

    # Create context with malicious HTML in multiple user-derived fields
    context = ReportContext(
        source_name="</p><script>alert(1)</script><p>evil.csv",
        column_name="Price < Discount & <b>weird</b>",
        preprocessing_options=PreprocessingOptions(),
        preprocessing_preview=preview,
        suitability=assessment,
        result=result,
        result_summary="Close to Benford</p><img src=x onerror='alert(2)'>",
        chart_figure=figure,
    )

    html = render_html_report(context)

    # Verify raw HTML tags are NOT present in the output (unescaped)
    assert "<script>" not in html
    assert "</p><script>" not in html
    assert "<img src=x onerror=" not in html  # the dangerous img tag unescaped

    # Verify escaped forms ARE present (source_name, column_name, result_summary)
    assert "&lt;script&gt;" in html
    assert "&lt;b&gt;" in html
    assert "Price &lt; Discount" in html
    assert "&lt;img src=x onerror=" in html  # the img tag should be escaped
