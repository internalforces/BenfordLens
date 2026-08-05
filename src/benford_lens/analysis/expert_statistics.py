"""Expert statistics for a first-digit Benford analysis.

The values returned here are descriptive/reference statistics only. This
module does not decide whether Benford's Law applies to a dataset and does
not attach an automated interpretation to any statistic or p-value.
"""

from __future__ import annotations

import math
from collections.abc import Iterable
from dataclasses import dataclass

import numpy as np
from scipy.stats import chisquare, kstest

from benford_lens.analysis.benford import BenfordResult

_DIGITS: tuple[int, ...] = tuple(range(1, 10))


@dataclass(frozen=True)
class ExpertStatistics:
    """Reference statistics calculated from one Benford analysis snapshot."""

    sample_size: int
    mean_absolute_deviation: float | None
    chi_square_statistic: float | None
    chi_square_p_value: float | None
    ks_statistic: float | None
    ks_p_value: float | None


def _log_mantissas(values: Iterable[float]) -> np.ndarray:
    """Return fractional base-10 logarithms for finite, non-zero magnitudes.

    Benford-distributed positive magnitudes have uniformly distributed
    fractional ``log10`` parts. Testing those parts avoids applying the
    continuous KS p-value formula directly to the discrete leading digits.
    """
    magnitudes = np.asarray(
        [abs(float(value)) for value in values if math.isfinite(float(value)) and value != 0],
        dtype=float,
    )
    logarithms = np.log10(magnitudes)
    return logarithms - np.floor(logarithms)


def calculate_expert_statistics(values: Iterable[float], result: BenfordResult) -> ExpertStatistics:
    """Calculate MAD, Chi-square and KS statistics for one analysis.

    ``values`` must be the same preprocessed values used to produce
    ``result``. MAD and Chi-square compare the observed first-digit buckets
    with Benford's expected buckets. KS compares the values' base-10 log
    mantissas with a continuous uniform distribution, an equivalent form of
    Benford's Law that supports the one-sample KS calculation.

    Empty inputs return ``None`` for every statistic instead of exposing
    SciPy's undefined NaN results.
    """
    if result.sample_size == 0:
        return ExpertStatistics(
            sample_size=0,
            mean_absolute_deviation=None,
            chi_square_statistic=None,
            chi_square_p_value=None,
            ks_statistic=None,
            ks_p_value=None,
        )

    observed_proportions = np.asarray(
        [result.observed_proportions[digit] for digit in _DIGITS], dtype=float
    )
    expected_proportions = np.asarray(
        [result.expected_proportions[digit] for digit in _DIGITS], dtype=float
    )
    mean_absolute_deviation = float(np.mean(np.abs(observed_proportions - expected_proportions)))

    observed_counts = np.asarray([result.observed_counts[digit] for digit in _DIGITS], dtype=float)
    # Normalizing first makes the expected counts sum to the observed total
    # even if a custom BenfordResult carries tiny floating-point drift.
    expected_counts = expected_proportions / expected_proportions.sum() * result.sample_size
    chi_square = chisquare(observed_counts, expected_counts)

    log_mantissas = _log_mantissas(values)
    ks = kstest(log_mantissas, "uniform")

    return ExpertStatistics(
        sample_size=result.sample_size,
        mean_absolute_deviation=mean_absolute_deviation,
        chi_square_statistic=float(chi_square.statistic),
        chi_square_p_value=float(chi_square.pvalue),
        ks_statistic=float(ks.statistic),
        ks_p_value=float(ks.pvalue),
    )
