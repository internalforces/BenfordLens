"""Expected-vs-actual first-digit chart and a structured result summary.

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


@dataclass(frozen=True)
class ResultSummary:
    """A summary sentence as a stable code plus the numbers behind it."""

    code: str
    params: dict[str, object] = field(default_factory=dict)


def build_first_digit_figure(result: BenfordResult) -> Figure:
    """Build a bar-plus-line chart comparing observed vs. expected proportions."""
    digits = sorted(result.expected_proportions)
    observed = [result.observed_proportions[d] * 100 for d in digits]
    expected = [result.expected_proportions[d] * 100 for d in digits]

    figure = Figure(figsize=(6, 4))
    axes = figure.add_subplot(111)
    axes.bar(digits, observed, color="#4C72B0", label="Observed")
    axes.plot(digits, expected, color="black", marker="o", label="Expected (Benford)")
    axes.set_xlabel("Leading digit")
    axes.set_ylabel("Proportion (%)")
    axes.set_xticks(digits)
    axes.legend()
    figure.tight_layout()
    return figure


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
