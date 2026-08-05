from pathlib import Path

from matplotlib.figure import Figure

from benford_lens.analysis.benford import analyze_first_digit
from benford_lens.charts import benford_chart
from benford_lens.charts.benford_chart import (
    SUMMARY_CLOSE_TO_BENFORD,
    SUMMARY_DIVERGES_FROM_BENFORD,
    SUMMARY_NO_VALID_VALUES,
    SUMMARY_SAMPLE_TOO_SMALL,
    build_first_digit_figure,
    summarize_result,
)


def test_build_first_digit_figure_returns_a_figure_with_one_axes():
    result = analyze_first_digit([111, 111, 222, 333])

    figure = build_first_digit_figure(result)

    assert isinstance(figure, Figure)
    assert len(figure.axes) == 1


def test_summarize_result_flags_empty_sample():
    result = analyze_first_digit([])

    summary = summarize_result(result)

    assert summary.code == SUMMARY_NO_VALID_VALUES
    assert summary.params == {}


def test_summarize_result_flags_divergence_for_a_skewed_sample():
    skewed_result = analyze_first_digit([9] * 50 + [1])

    summary = summarize_result(skewed_result)

    assert summary.code == SUMMARY_DIVERGES_FROM_BENFORD


def test_summarize_result_flags_small_sample_as_not_meaningful():
    small_result = analyze_first_digit([12, 13, 14])

    summary = summarize_result(small_result)

    assert summary.code == SUMMARY_SAMPLE_TOO_SMALL
    assert summary.params == {"sample_size": 3}


def test_summarize_result_flags_a_close_match_for_a_large_benford_like_sample():
    # Regression test for TD-002 (memory/known-issues.md): no test previously
    # exercised the "close to the expected Benford distribution" branch of
    # summarize_result — the >=30-sample test above actually hit the
    # small-sample branch instead. Powers of 2 are a classic sample whose
    # leading digits closely follow Benford's Law.
    close_result = analyze_first_digit([2**k for k in range(1, 101)])

    assert close_result.sample_size >= 30
    assert summarize_result(close_result).code == SUMMARY_CLOSE_TO_BENFORD


def test_chart_module_contains_no_user_facing_summary_prose():
    # Guard for the architecture rule: summarize_result returns a code plus
    # numbers so the presentation layer owns (and can translate) the wording.
    source = Path(benford_chart.__file__).read_text(encoding="utf-8")
    for phrase in (
        "No valid numeric values were found",
        "Try a column with more data",
        "The overall distribution",
    ):
        assert phrase not in source
