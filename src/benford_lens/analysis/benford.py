"""First-digit Benford's Law analysis (Analysis Engine — no UI dependency).

This module never decides whether Benford's Law "applies" to a dataset;
it only computes the observed vs. expected leading-digit distribution and
leaves interpretation to the user, per AGENTS.md.
"""

from __future__ import annotations

import math
from collections.abc import Iterable
from dataclasses import dataclass

import pandas as pd

_DIGITS: tuple[int, ...] = tuple(range(1, 10))


def expected_first_digit_distribution() -> dict[int, float]:
    """Return Benford's Law's expected proportion for each leading digit 1-9."""
    return {d: math.log10(1 + 1 / d) for d in _DIGITS}


def first_digit(value: float | int | None) -> int | None:
    """Return the leading significant digit of a number, or None if undefined.

    None is returned for missing values, NaN, +/-infinity, and zero — none
    of these have a meaningful leading digit for Benford's Law.
    """
    if value is None:
        return None
    numeric_value = float(value)
    # math.isfinite() is False for both NaN and +/-inf, so this one check
    # covers the missing/undefined cases in a single branch. Without it,
    # float("inf") formats as "inf" and int("i") raises ValueError.
    if not math.isfinite(numeric_value):
        return None
    magnitude = abs(numeric_value)
    if magnitude == 0:
        return None
    mantissa = f"{magnitude:.15e}"
    return int(mantissa[0])


@dataclass
class BenfordResult:
    observed_counts: dict[int, int]
    observed_proportions: dict[int, float]
    expected_proportions: dict[int, float]
    sample_size: int


def analyze_first_digit(series: Iterable[float] | pd.Series) -> BenfordResult:
    """Compute observed vs. expected first-digit distribution for a column."""
    digits = [d for d in (first_digit(value) for value in series) if d is not None]
    sample_size = len(digits)

    counts = {d: 0 for d in _DIGITS}
    for digit in digits:
        counts[digit] += 1

    proportions = {d: (counts[d] / sample_size if sample_size else 0.0) for d in _DIGITS}

    return BenfordResult(
        observed_counts=counts,
        observed_proportions=proportions,
        expected_proportions=expected_first_digit_distribution(),
        sample_size=sample_size,
    )
