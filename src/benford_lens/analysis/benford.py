"""Digit-position Benford's Law analysis (Analysis Engine — no UI dependency).

This module never decides whether Benford's Law "applies" to a dataset;
it only computes observed vs. expected significant-digit distributions and
leaves interpretation to the user. Existing first-digit entry
points remain available as compatibility-preserving public APIs.
"""

from __future__ import annotations

import math
from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum

import pandas as pd

_FIRST_DIGITS: tuple[int, ...] = tuple(range(1, 10))
_SECOND_DIGITS: tuple[int, ...] = tuple(range(10))

MIN_MEANINGFUL_SAMPLE = 30


class DigitPosition(Enum):
    """Supported significant-digit positions."""

    FIRST = "first"
    SECOND = "second"


def expected_first_digit_distribution() -> dict[int, float]:
    """Return Benford's Law's expected proportion for each leading digit 1-9."""
    return {digit: math.log10(1 + 1 / digit) for digit in _FIRST_DIGITS}


def expected_second_digit_distribution() -> dict[int, float]:
    """Return Benford's expected proportion for each second digit 0-9."""
    return {
        digit: sum(
            math.log10(1 + 1 / (10 * first_digit_value + digit))
            for first_digit_value in _FIRST_DIGITS
        )
        for digit in _SECOND_DIGITS
    }


def _significant_digits(value: float | int | None) -> tuple[int, int] | None:
    """Return the first two normalized significant digits when they exist."""
    if value is None:
        return None
    numeric_value = float(value)
    if not math.isfinite(numeric_value):
        return None
    magnitude = abs(numeric_value)
    if magnitude == 0:
        return None

    # Scientific notation makes the intended normalization explicit: a value
    # such as 5 is represented as 5.0 × 10^0 and therefore has second digit 0.
    mantissa = f"{magnitude:.15e}"
    return int(mantissa[0]), int(mantissa[2])


def first_digit(value: float | int | None) -> int | None:
    """Return the leading significant digit of a number, or None if undefined.

    None is returned for missing values, NaN, +/-infinity, and zero — none
    of these have a meaningful leading digit for Benford's Law.
    """
    digits = _significant_digits(value)
    return None if digits is None else digits[0]


def second_digit(value: float | int | None) -> int | None:
    """Return the second significant digit of a number, or None if undefined.

    A magnitude with one explicit significant digit contributes zero in the
    second position because its normalized representation includes a trailing
    zero, for example ``5.0 × 10^0``.
    """
    digits = _significant_digits(value)
    return None if digits is None else digits[1]


@dataclass
class BenfordResult:
    observed_counts: dict[int, int]
    observed_proportions: dict[int, float]
    expected_proportions: dict[int, float]
    sample_size: int


@dataclass(frozen=True)
class CombinedBenfordResult:
    """Independent first- and second-digit results from one source pass."""

    first: BenfordResult
    second: BenfordResult


def _build_result(
    digits: list[int],
    buckets: tuple[int, ...],
    expected_proportions: dict[int, float],
) -> BenfordResult:
    """Aggregate extracted digits into one observed/expected result."""
    sample_size = len(digits)
    counts = {digit: 0 for digit in buckets}
    for digit in digits:
        counts[digit] += 1

    proportions = {
        digit: (counts[digit] / sample_size if sample_size else 0.0) for digit in buckets
    }
    return BenfordResult(
        observed_counts=counts,
        observed_proportions=proportions,
        expected_proportions=expected_proportions,
        sample_size=sample_size,
    )


def analyze_first_digit(series: Iterable[float] | pd.Series) -> BenfordResult:
    """Compute observed vs. expected first-digit distribution for a column."""
    digits = [d for d in (first_digit(value) for value in series) if d is not None]
    return _build_result(
        digits,
        _FIRST_DIGITS,
        expected_first_digit_distribution(),
    )


def analyze_second_digit(series: Iterable[float] | pd.Series) -> BenfordResult:
    """Compute observed vs. expected second-digit distribution for a column."""
    digits = [d for d in (second_digit(value) for value in series) if d is not None]
    return _build_result(
        digits,
        _SECOND_DIGITS,
        expected_second_digit_distribution(),
    )


def analyze_combined(series: Iterable[float] | pd.Series) -> CombinedBenfordResult:
    """Compute first- and second-digit results together in one source pass."""
    result, _digit_pairs = analyze_combined_with_digit_pairs(series)
    return result


def analyze_combined_with_digit_pairs(
    series: Iterable[float] | pd.Series,
) -> tuple[CombinedBenfordResult, tuple[tuple[int, int] | None, ...]]:
    """Compute combined results and aligned digit pairs in one source pass.

    The aligned pairs let workflow layers build drill-down mappings without
    repeating significant-digit extraction. Invalid values retain a ``None``
    placeholder so the returned tuple stays aligned with the input order.
    """
    first_digits: list[int] = []
    second_digits: list[int] = []
    digit_pairs: list[tuple[int, int] | None] = []
    for value in series:
        digits = _significant_digits(value)
        digit_pairs.append(digits)
        if digits is None:
            continue
        first, second = digits
        first_digits.append(first)
        second_digits.append(second)

    return (
        CombinedBenfordResult(
            first=_build_result(
                first_digits,
                _FIRST_DIGITS,
                expected_first_digit_distribution(),
            ),
            second=_build_result(
                second_digits,
                _SECOND_DIGITS,
                expected_second_digit_distribution(),
            ),
        ),
        tuple(digit_pairs),
    )
