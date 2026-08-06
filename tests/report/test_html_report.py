from matplotlib.figure import Figure

from benford_lens.analysis.benford import (
    BenfordResult,
    analyze_combined,
    analyze_second_digit,
)
from benford_lens.analysis.expert_statistics import calculate_combined_expert_statistics
from benford_lens.analysis.preprocessing import PreprocessingOptions, PreprocessingPreview
from benford_lens.analysis.suitability import (
    NOTE_NARROW_MAGNITUDE_RANGE,
    SuitabilityAssessment,
    SuitabilityLevel,
    SuitabilityMetrics,
    SuitabilityNote,
)
from benford_lens.charts.benford_chart import (
    SUMMARY_CLOSE_TO_BENFORD,
    ResultSummary,
    build_digit_figure,
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

    restricted_fragments = (
        "fr" + "aud",
        "fr" + "audulent",
        "manip" + "ulated",
        "manip" + "ulation",
    )
    assert all(fragment not in html for fragment in restricted_fragments)


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


def test_render_html_report_shows_the_sheet_name_for_excel_sources():
    context = _build_context()
    context.source_name = "workbook.xlsx"
    context.sheet_name = "Q3 & Q4 <ledger>"

    html = render_html_report(context)

    assert "Sheet: Q3 &amp; Q4 &lt;ledger&gt;" in html
    assert "<ledger>" not in html


def test_render_html_report_omits_the_sheet_fragment_for_csv_sources():
    html = render_html_report(_build_context())

    assert "Sheet:" not in html
    assert "Source: sample.csv — Column: amount" in html


def test_render_second_digit_report_uses_zero_to_nine_distribution():
    context = _build_context()
    second_result = analyze_second_digit([101, 105, 111, 222])
    context.mode = "second"
    context.result = second_result
    context.result_summary = ResultSummary(SUMMARY_CLOSE_TO_BENFORD)
    context.chart_figure = build_digit_figure(second_result, x_axis_label="Second digit")

    html = render_html_report(context)

    assert "Second-digit distribution" in html
    assert "First-digit distribution" not in html
    assert "<tr><td>0</td>" in html
    assert "<tr><td>9</td>" in html


def test_render_combined_report_contains_both_results_and_shared_context_once():
    values = [101.0, 105.0, 111.0, 222.0]
    combined = analyze_combined(values)
    context = _build_context()
    context.mode = "combined"
    context.result = combined.first
    context.result_summary = ResultSummary(SUMMARY_CLOSE_TO_BENFORD)
    context.chart_figure = build_digit_figure(combined.first, x_axis_label="First digit")
    context.second_result = combined.second
    context.second_result_summary = ResultSummary(SUMMARY_CLOSE_TO_BENFORD)
    context.second_chart_figure = build_digit_figure(combined.second, x_axis_label="Second digit")
    context.expert_statistics = calculate_combined_expert_statistics(values, combined)

    html = render_html_report(context)

    assert html.count("First-digit distribution") == 1
    assert html.count("Second-digit distribution") == 1
    assert html.count("data:image/png;base64,") == 2
    assert html.count("<h2>Preprocessing</h2>") == 1
    assert html.count("<h2>Data suitability</h2>") == 1
    assert html.count("Shared KS statistic") == 1
    assert html.count("This report was generated entirely") == 1
