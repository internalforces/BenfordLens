"""Expected-vs-actual digit charts and structured result summaries.

This module is UI-agnostic Matplotlib code, so like the Analysis Engine it
does not own user-facing prose: summarize_result() returns a code plus its
numbers, and the presentation layer renders it in the user's language. The
templates it maps to follow AGENTS.md's Product Philosophy & Tone Rules:
neutral and exploratory, never accusatory or conclusive.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from matplotlib import font_manager
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties

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
_DEFAULT_FONT_CANDIDATES = ("Arial Unicode MS", "DejaVu Sans")
_KOREAN_FONT_CANDIDATES = (
    "Malgun Gothic",
    "Apple SD Gothic Neo",
    "Noto Sans CJK KR",
)
_CHINESE_FONT_CANDIDATES = (
    "Microsoft YaHei",
    "Microsoft JhengHei",
    "PingFang SC",
    "Noto Sans CJK SC",
)
_JAPANESE_FONT_CANDIDATES = (
    "Yu Gothic",
    "Meiryo",
    "Hiragino Sans",
    "Noto Sans CJK JP",
)


def _font_candidates_for_text(text: str) -> tuple[str, ...]:
    """Return platform-friendly font candidates for the scripts in *text*."""
    codepoints = (ord(character) for character in text)
    if any(0xAC00 <= codepoint <= 0xD7AF for codepoint in codepoints):
        return _KOREAN_FONT_CANDIDATES + _DEFAULT_FONT_CANDIDATES

    codepoints = (ord(character) for character in text)
    if any(
        0x3040 <= codepoint <= 0x30FF or 0x31F0 <= codepoint <= 0x31FF for codepoint in codepoints
    ):
        return _JAPANESE_FONT_CANDIDATES + _DEFAULT_FONT_CANDIDATES

    codepoints = (ord(character) for character in text)
    if any(0x3400 <= codepoint <= 0x9FFF for codepoint in codepoints):
        return _CHINESE_FONT_CANDIDATES + _DEFAULT_FONT_CANDIDATES
    return _DEFAULT_FONT_CANDIDATES


def _font_properties(text: str) -> FontProperties:
    """Choose the first installed font suitable for a translated chart label."""
    installed_families = {font.name for font in font_manager.fontManager.ttflist}
    family = next(
        (name for name in _font_candidates_for_text(text) if name in installed_families),
        "DejaVu Sans",
    )
    return FontProperties(family=family)


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
    axes.set_xlabel(x_axis_label, fontproperties=_font_properties(x_axis_label))
    axes.set_ylabel(y_axis_label, fontproperties=_font_properties(y_axis_label))
    axes.set_xticks(digits)
    legend_text = f"{observed_label} {expected_label}"
    axes.legend(prop=_font_properties(legend_text))
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
