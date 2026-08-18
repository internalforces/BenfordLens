from pathlib import Path

from matplotlib.figure import Figure

from benford_lens.analysis.benford import analyze_first_digit, analyze_second_digit
from benford_lens.charts import benford_chart
from benford_lens.charts.benford_chart import (
    SUMMARY_CLOSE_TO_BENFORD,
    SUMMARY_DIVERGES_FROM_BENFORD,
    SUMMARY_NO_VALID_VALUES,
    SUMMARY_SAMPLE_TOO_SMALL,
    build_digit_figure,
    build_first_digit_figure,
    summarize_result,
)


def test_build_first_digit_figure_returns_a_figure_with_one_axes():
    result = analyze_first_digit([111, 111, 222, 333])

    figure = build_first_digit_figure(result)

    assert isinstance(figure, Figure)
    assert len(figure.axes) == 1


def test_build_digit_figure_supports_second_digit_buckets_and_labels():
    result = analyze_second_digit([101, 111, 222, 5])

    figure = build_digit_figure(result, x_axis_label="Second digit")

    axes = figure.axes[0]
    assert list(axes.get_xticks()) == list(range(10))
    assert axes.get_xlabel() == "Second digit"


def test_chart_selects_installed_windows_fonts_for_cjk_labels(monkeypatch):
    installed_fonts = [
        type("Font", (), {"name": name})()
        for name in ("Malgun Gothic", "Microsoft YaHei", "Yu Gothic", "DejaVu Sans")
    ]
    monkeypatch.setattr(benford_chart.font_manager.fontManager, "ttflist", installed_fonts)

    assert benford_chart._font_properties("선행 숫자").get_family() == ["Malgun Gothic"]
    assert benford_chart._font_properties("首位数字").get_family() == ["Microsoft YaHei"]
    assert benford_chart._font_properties("先頭の数字").get_family() == ["Yu Gothic"]


def test_chart_font_falls_back_to_dejavu_when_cjk_font_is_unavailable(monkeypatch):
    installed_fonts = [type("Font", (), {"name": "DejaVu Sans"})()]
    monkeypatch.setattr(benford_chart.font_manager.fontManager, "ttflist", installed_fonts)

    assert benford_chart._font_properties("선행 숫자").get_family() == ["DejaVu Sans"]


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
    # Regression coverage for summarize_result's "close to the expected
    # Benford distribution" branch — the >=30-sample test above actually hit the
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
