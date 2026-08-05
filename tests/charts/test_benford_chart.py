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

    for banned_word in ("fraud", "fraudulent", "manipulated"):
        assert banned_word not in summary.lower()


def test_summarize_result_flags_divergence_for_a_skewed_sample():
    skewed_result = analyze_first_digit([9] * 50 + [1])

    summary = summarize_result(skewed_result)

    assert "differs" in summary.lower()
    # The pre-approved neutral phrasing from AGENTS.md's tone rules must
    # actually appear somewhere in the product, not just be absent of
    # banned words.
    assert "This result alone cannot be used to judge data errors or manipulation" in summary


def test_summarize_result_flags_small_sample_as_not_meaningful():
    small_result = analyze_first_digit([12, 13, 14])

    summary = summarize_result(small_result)

    assert "too few" in summary.lower()
    for banned_word in ("fraud", "fraudulent", "manipulated"):
        assert banned_word not in summary.lower()


def test_summarize_result_flags_a_close_match_for_a_large_benford_like_sample():
    # Regression test for TD-002 (memory/known-issues.md): no test previously
    # exercised the "close to the expected Benford distribution" branch of
    # summarize_result — the >=30-sample test above actually hit the
    # small-sample branch instead. Powers of 2 are a classic sample whose
    # leading digits closely follow Benford's Law.
    close_result = analyze_first_digit([2**k for k in range(1, 101)])

    summary = summarize_result(close_result)

    assert close_result.sample_size >= 30
    assert "close to the expected benford distribution" in summary.lower()
    assert "This result alone cannot be used to judge data errors or manipulation" in summary
    for banned_word in ("fraud", "fraudulent", "manipulated"):
        assert banned_word not in summary.lower()
