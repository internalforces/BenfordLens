"""Expected-vs-actual first-digit chart and plain-language result summary.

Summary wording follows AGENTS.md's Product Philosophy & Tone Rules: neutral
and exploratory, never accusatory or conclusive about data manipulation.
"""

from __future__ import annotations

from matplotlib.figure import Figure

from benford_lens.analysis.benford import MIN_MEANINGFUL_SAMPLE, BenfordResult

# MVP heuristic: flags a >2 percentage-point gap on any single digit; M2's
# suitability check (TASK-008) will replace this with proper statistical
# tests (MAD/Chi-square/KS).
_DIVERGENCE_THRESHOLD = 0.02


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


def summarize_result(result: BenfordResult) -> str:
    """Produce a neutral, exploratory plain-language summary of the result."""
    if result.sample_size == 0:
        return "No valid numeric values were found in the selected column."

    if result.sample_size < MIN_MEANINGFUL_SAMPLE:
        return (
            f"Only {result.sample_size} valid numeric value(s) were found, which is too few "
            "for a meaningful comparison to the expected Benford distribution. "
            "Try a column with more data."
        )

    max_gap = max(
        abs(result.observed_proportions[d] - result.expected_proportions[d])
        for d in result.expected_proportions
    )

    if max_gap < _DIVERGENCE_THRESHOLD:
        return (
            "The overall distribution is close to the expected Benford distribution. "
            "This result alone cannot be used to judge data errors or manipulation."
        )
    return (
        "The overall distribution differs somewhat from the expected Benford distribution. "
        "This result alone cannot be used to judge data errors or manipulation; "
        "further review may be warranted."
    )
