"""Expected-vs-actual digit charts and structured result summaries.

This module is UI-agnostic Matplotlib code, so like the Analysis Engine it
does not own user-facing prose: summarize_result() returns a code plus its
numbers, and the presentation layer renders it in the user's language. The
templates it maps to follow AGENTS.md's Product Philosophy & Tone Rules:
neutral and exploratory, never accusatory or conclusive.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from matplotlib.figure import Figure

from benford_lens.analysis.benford import MIN_MEANINGFUL_SAMPLE, BenfordResult

# MVP heuristic: flags a >2 percentage-point gap on any single digit; M2's
# suitability check (TASK-008) will replace this with proper statistical
# tests (MAD/Chi-square/KS).
_DIVERGENCE_THRESHOLD = 0.02

# Stable identifiers for the summary sentences the presentation layer can
# render; nothing here knows what they say in any language.
SUMMARY_NO_VALID_VALUES = "NO_VALID_VALUES"
SUMMARY_SAMPLE_TOO_SMALL = "SAMPLE_TOO_SMALL"
SUMMARY_CLOSE_TO_BENFORD = "CLOSE_TO_BENFORD"
SUMMARY_DIVERGES_FROM_BENFORD = "DIVERGES_FROM_BENFORD"

# Prefer a broad Unicode font where the host provides one, while retaining
# Matplotlib's bundled DejaVu Sans fallback for minimal installations.
_CHART_FONT_FAMILIES = [
    "Arial Unicode MS",
    "Apple SD Gothic Neo",
    "Noto Sans CJK KR",
    "Noto Sans CJK SC",
    "Noto Sans CJK JP",
    "DejaVu Sans",
]


@dataclass(frozen=True)
class ResultSummary:
    """A summary sentence as a stable code plus the numbers behind it."""

    code: str
    params: dict[str, object] = field(default_factory=dict)


def build_digit_figure(
    result: BenfordResult,
    *,
    x_axis_label: str = "Digit",
    y_axis_label: str = "Proportion (%)",
    observed_label: str = "Observed",
    expected_label: str = "Expected (Benford)",
) -> Figure:
    """Build a position-neutral observed-vs-expected digit chart."""
    digits = sorted(result.expected_proportions)
    observed = [result.observed_proportions[d] * 100 for d in digits]
    expected = [result.expected_proportions[d] * 100 for d in digits]

    figure = Figure(figsize=(6, 4))
    axes = figure.add_subplot(111)
    axes.bar(digits, observed, color="#4C72B0", label=observed_label)
    axes.plot(digits, expected, color="black", marker="o", label=expected_label)
    axes.set_xlabel(x_axis_label, fontfamily=_CHART_FONT_FAMILIES)
    axes.set_ylabel(y_axis_label, fontfamily=_CHART_FONT_FAMILIES)
    axes.set_xticks(digits)
    axes.legend(prop={"family": _CHART_FONT_FAMILIES})
    figure.tight_layout()
    return figure


def build_first_digit_figure(result: BenfordResult) -> Figure:
    """Build the existing first-digit chart (compatibility wrapper)."""
    return build_digit_figure(result, x_axis_label="Leading digit")


def summarize_result(result: BenfordResult) -> ResultSummary:
    """Classify the result into one of the summary codes."""
    if result.sample_size == 0:
        return ResultSummary(SUMMARY_NO_VALID_VALUES)

    if result.sample_size < MIN_MEANINGFUL_SAMPLE:
        return ResultSummary(SUMMARY_SAMPLE_TOO_SMALL, {"sample_size": result.sample_size})

    max_gap = max(
        abs(result.observed_proportions[d] - result.expected_proportions[d])
        for d in result.expected_proportions
    )

    if max_gap < _DIVERGENCE_THRESHOLD:
        return ResultSummary(SUMMARY_CLOSE_TO_BENFORD)
    return ResultSummary(SUMMARY_DIVERGES_FROM_BENFORD)
