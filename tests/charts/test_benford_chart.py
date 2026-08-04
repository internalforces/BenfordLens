from matplotlib.figure import Figure

from benford_lens.analysis.benford import analyze_first_digit
from benford_lens.charts.benford_chart import build_first_digit_figure, summarize_result


def test_build_first_digit_figure_returns_a_figure_with_one_axes():
    result = analyze_first_digit([111, 111, 222, 333])

    figure = build_first_digit_figure(result)

    assert isinstance(figure, Figure)
    assert len(figure.axes) == 1


def test_summarize_result_flags_empty_sample():
    result = analyze_first_digit([])

    summary = summarize_result(result)

    assert "no valid" in summary.lower()


def test_summarize_result_uses_neutral_non_accusatory_language():
    close_result = analyze_first_digit([12, 13, 14, 15, 18, 19, 21, 31, 41, 91])

    summary = summarize_result(close_result)

    for banned_word in ("fraud", "fraudulent"):
        assert banned_word not in summary.lower()


def test_summarize_result_flags_divergence_for_a_skewed_sample():
    skewed_result = analyze_first_digit([9] * 50 + [1])

    summary = summarize_result(skewed_result)

    assert "differs" in summary.lower()
