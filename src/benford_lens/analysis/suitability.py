"""Data suitability check (Analysis Engine — no UI dependency).

This module surfaces data characteristics as an advisory signal only. It
never states or implies whether Benford's Law applies to a dataset — that
judgment always belongs to the user, per AGENTS.md.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum

import pandas as pd

from benford_lens.analysis.benford import MIN_MEANINGFUL_SAMPLE

# See ADR-006 (memory/decisions.md) for the rationale behind these
# thresholds — heuristic advisory defaults, not a statistical test.
_GOOD_SAMPLE_COUNT = 300
_GOOD_DIGIT_RANGE = 4
_GOOD_DISTINCT_RATIO = 0.3
_CAUTION_DISTINCT_RATIO = 0.1
_ZERO_RATE_CAUTION = 0.3
_NEGATIVE_RATE_CAUTION = 0.5
_MISSING_RATE_CAUTION = 0.3


class SuitabilityLevel(Enum):
    GOOD = "good"
    CAUTION = "caution"
    DIFFICULT = "difficult"


@dataclass
class SuitabilityMetrics:
    sample_count: int
    min_value: float | None
    max_value: float | None
    digit_range: int
    duplicate_rate: float
    zero_rate: float
    negative_rate: float
    missing_rate: float
    distinct_value_count: int


@dataclass
class SuitabilityAssessment:
    level: SuitabilityLevel
    metrics: SuitabilityMetrics
    notes: list[str]


def _digit_range(values: pd.Series) -> int:
    finite = values[values.apply(math.isfinite)]
    nonzero = finite[finite != 0]
    if nonzero.empty:
        return 0
    buckets = nonzero.abs().map(lambda v: math.floor(math.log10(v)) + 1)
    return int(buckets.nunique())


def compute_suitability_metrics(
    preprocessed_series: pd.Series, raw_series: pd.Series
) -> SuitabilityMetrics:
    raw_total = len(raw_series)
    missing_rate = float(raw_series.isna().sum() / raw_total) if raw_total else 0.0

    raw_numeric = pd.to_numeric(raw_series, errors="coerce")
    zero_rate = float((raw_numeric == 0).sum() / raw_total) if raw_total else 0.0
    negative_rate = float((raw_numeric < 0).sum() / raw_total) if raw_total else 0.0

    raw_distinct = int(raw_series.nunique(dropna=True))
    duplicate_rate = float(1 - raw_distinct / raw_total) if raw_total else 0.0

    sample_count = len(preprocessed_series)
    min_value = float(preprocessed_series.min()) if sample_count else None
    max_value = float(preprocessed_series.max()) if sample_count else None

    return SuitabilityMetrics(
        sample_count=sample_count,
        min_value=min_value,
        max_value=max_value,
        digit_range=_digit_range(preprocessed_series),
        duplicate_rate=duplicate_rate,
        zero_rate=zero_rate,
        negative_rate=negative_rate,
        missing_rate=missing_rate,
        distinct_value_count=int(preprocessed_series.nunique()),
    )


def assess_suitability(metrics: SuitabilityMetrics) -> SuitabilityAssessment:
    distinct_ratio = (
        metrics.distinct_value_count / metrics.sample_count if metrics.sample_count else 0.0
    )

    levels = [SuitabilityLevel.GOOD]
    notes: list[str] = []

    if metrics.sample_count < MIN_MEANINGFUL_SAMPLE:
        levels.append(SuitabilityLevel.DIFFICULT)
        notes.append(
            f"Only {metrics.sample_count} valid value(s) — below the "
            f"{MIN_MEANINGFUL_SAMPLE}-value floor for a meaningful comparison."
        )
    elif metrics.sample_count < _GOOD_SAMPLE_COUNT:
        levels.append(SuitabilityLevel.CAUTION)
        notes.append(f"{metrics.sample_count} valid values is a workable but modest sample size.")

    if metrics.digit_range <= 1:
        levels.append(SuitabilityLevel.DIFFICULT)
        notes.append("Values span only a single order of magnitude.")
    elif metrics.digit_range < _GOOD_DIGIT_RANGE:
        levels.append(SuitabilityLevel.CAUTION)
        notes.append(f"Values span {metrics.digit_range} orders of magnitude.")

    if distinct_ratio < _CAUTION_DISTINCT_RATIO:
        levels.append(SuitabilityLevel.DIFFICULT)
        notes.append("Very few distinct values relative to the sample size.")
    elif distinct_ratio < _GOOD_DISTINCT_RATIO:
        levels.append(SuitabilityLevel.CAUTION)
        notes.append("Values repeat somewhat more than expected for this sample size.")

    if metrics.zero_rate > _ZERO_RATE_CAUTION:
        levels.append(SuitabilityLevel.CAUTION)
        notes.append(f"{metrics.zero_rate:.0%} of the source values were zero.")
    if metrics.negative_rate > _NEGATIVE_RATE_CAUTION:
        levels.append(SuitabilityLevel.CAUTION)
        notes.append(
            f"{metrics.negative_rate:.0%} of the source values were negative — check "
            "whether the negative-value preprocessing option fits this data."
        )
    if metrics.missing_rate > _MISSING_RATE_CAUTION:
        levels.append(SuitabilityLevel.CAUTION)
        notes.append(f"{metrics.missing_rate:.0%} of the source values were blank.")

    if SuitabilityLevel.DIFFICULT in levels:
        overall = SuitabilityLevel.DIFFICULT
    elif SuitabilityLevel.CAUTION in levels:
        overall = SuitabilityLevel.CAUTION
    else:
        overall = SuitabilityLevel.GOOD

    return SuitabilityAssessment(level=overall, metrics=metrics, notes=notes)
