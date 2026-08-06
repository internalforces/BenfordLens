"""Reference statistics for first- and second-digit Benford analyses.

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

from benford_lens.analysis.benford import BenfordResult, CombinedBenfordResult


@dataclass(frozen=True)
class ExpertStatistics:
    """Reference statistics calculated from one Benford analysis snapshot."""

    sample_size: int
    mean_absolute_deviation: float | None
    chi_square_statistic: float | None
    chi_square_p_value: float | None
    ks_statistic: float | None
    ks_p_value: float | None


@dataclass(frozen=True)
class DistributionStatistics:
    """MAD and Chi-square values for one digit-position distribution."""

    sample_size: int
    mean_absolute_deviation: float | None
    chi_square_statistic: float | None
    chi_square_p_value: float | None


@dataclass(frozen=True)
class LogMantissaStatistics:
    """One shared KS comparison for the preprocessed numeric sample."""

    sample_size: int
    ks_statistic: float | None
    ks_p_value: float | None


@dataclass(frozen=True)
class CombinedExpertStatistics:
    """Per-position distribution values plus one sample-level KS result."""

    first: DistributionStatistics
    second: DistributionStatistics
    log_mantissa: LogMantissaStatistics


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


def calculate_distribution_statistics(result: BenfordResult) -> DistributionStatistics:
    """Calculate MAD and Chi-square for the buckets carried by ``result``."""
    if result.sample_size == 0:
        return DistributionStatistics(
            sample_size=0,
            mean_absolute_deviation=None,
            chi_square_statistic=None,
            chi_square_p_value=None,
        )

    # Dictionary insertion order is the public result's bucket order: 1-9 for
    # first digit and 0-9 for second digit. Deriving it from the result avoids
    # hard-coding either position into the statistics engine.
    buckets = tuple(result.expected_proportions)
    observed_proportions = np.asarray(
        [result.observed_proportions[digit] for digit in buckets], dtype=float
    )
    expected_proportions = np.asarray(
        [result.expected_proportions[digit] for digit in buckets], dtype=float
    )
    mean_absolute_deviation = float(np.mean(np.abs(observed_proportions - expected_proportions)))

    observed_counts = np.asarray([result.observed_counts[digit] for digit in buckets], dtype=float)
    # Normalize first so a custom result with tiny floating-point drift still
    # supplies expected counts whose sum exactly matches the observed total.
    expected_counts = expected_proportions / expected_proportions.sum() * result.sample_size
    chi_square = chisquare(observed_counts, expected_counts)

    return DistributionStatistics(
        sample_size=result.sample_size,
        mean_absolute_deviation=mean_absolute_deviation,
        chi_square_statistic=float(chi_square.statistic),
        chi_square_p_value=float(chi_square.pvalue),
    )


def calculate_log_mantissa_statistics(values: Iterable[float]) -> LogMantissaStatistics:
    """Calculate one KS comparison for the finite, non-zero magnitudes."""
    log_mantissas = _log_mantissas(values)
    sample_size = len(log_mantissas)
    if sample_size == 0:
        return LogMantissaStatistics(sample_size=0, ks_statistic=None, ks_p_value=None)

    ks = kstest(log_mantissas, "uniform")
    return LogMantissaStatistics(
        sample_size=sample_size,
        ks_statistic=float(ks.statistic),
        ks_p_value=float(ks.pvalue),
    )


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
    distribution = calculate_distribution_statistics(result)
    log_mantissa = calculate_log_mantissa_statistics(values)

    return ExpertStatistics(
        sample_size=result.sample_size,
        mean_absolute_deviation=distribution.mean_absolute_deviation,
        chi_square_statistic=distribution.chi_square_statistic,
        chi_square_p_value=distribution.chi_square_p_value,
        ks_statistic=log_mantissa.ks_statistic,
        ks_p_value=log_mantissa.ks_p_value,
    )


def calculate_combined_expert_statistics(
    values: Iterable[float], result: CombinedBenfordResult
) -> CombinedExpertStatistics:
    """Calculate per-position values and one shared KS result for combined mode."""
    return CombinedExpertStatistics(
        first=calculate_distribution_statistics(result.first),
        second=calculate_distribution_statistics(result.second),
        log_mantissa=calculate_log_mantissa_statistics(values),
    )
