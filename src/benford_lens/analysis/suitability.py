"""Data suitability check (Analysis Engine — no UI dependency).

This module surfaces data characteristics as an advisory signal only. It
never states or implies whether Benford's Law applies to a dataset — that
judgment always belongs to the user, per AGENTS.md.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
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

# Stable identifiers for the advisory notes assess_suitability() can emit.
# The presentation layer maps each to a translatable template; nothing in
# this module knows what any of them say in any language.
NOTE_SAMPLE_TOO_SMALL = "SAMPLE_TOO_SMALL"
NOTE_SAMPLE_MODEST = "SAMPLE_MODEST"
NOTE_SINGLE_MAGNITUDE = "SINGLE_MAGNITUDE"
NOTE_NARROW_MAGNITUDE_RANGE = "NARROW_MAGNITUDE_RANGE"
NOTE_LOW_DIVERSITY = "LOW_DIVERSITY"
NOTE_REPEATED_VALUES = "REPEATED_VALUES"
NOTE_HIGH_ZERO_RATE = "HIGH_ZERO_RATE"
NOTE_HIGH_NEGATIVE_RATE = "HIGH_NEGATIVE_RATE"
NOTE_HIGH_MISSING_RATE = "HIGH_MISSING_RATE"


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


@dataclass(frozen=True)
class SuitabilityNote:
    """One advisory observation, as a stable code plus the numbers behind it.

    Deliberately carries no prose. The Analysis Engine has no user-facing
    strings (AGENTS.md), and the presentation layer needs to be able to
    render these in the user's chosen language.
    """

    code: str
    params: dict[str, object] = field(default_factory=dict)


@dataclass
class SuitabilityAssessment:
    level: SuitabilityLevel
    metrics: SuitabilityMetrics
    notes: list[SuitabilityNote]


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
    notes: list[SuitabilityNote] = []

    if metrics.sample_count < MIN_MEANINGFUL_SAMPLE:
        levels.append(SuitabilityLevel.DIFFICULT)
        notes.append(
            SuitabilityNote(
                NOTE_SAMPLE_TOO_SMALL,
                {"sample_count": metrics.sample_count, "minimum": MIN_MEANINGFUL_SAMPLE},
            )
        )
    elif metrics.sample_count < _GOOD_SAMPLE_COUNT:
        levels.append(SuitabilityLevel.CAUTION)
        notes.append(SuitabilityNote(NOTE_SAMPLE_MODEST, {"sample_count": metrics.sample_count}))

    if metrics.digit_range <= 1:
        levels.append(SuitabilityLevel.DIFFICULT)
        notes.append(SuitabilityNote(NOTE_SINGLE_MAGNITUDE))
    elif metrics.digit_range < _GOOD_DIGIT_RANGE:
        levels.append(SuitabilityLevel.CAUTION)
        notes.append(
            SuitabilityNote(NOTE_NARROW_MAGNITUDE_RANGE, {"digit_range": metrics.digit_range})
        )

    if distinct_ratio < _CAUTION_DISTINCT_RATIO:
        levels.append(SuitabilityLevel.DIFFICULT)
        notes.append(SuitabilityNote(NOTE_LOW_DIVERSITY))
    elif distinct_ratio < _GOOD_DISTINCT_RATIO:
        levels.append(SuitabilityLevel.CAUTION)
        notes.append(SuitabilityNote(NOTE_REPEATED_VALUES))

    if metrics.zero_rate > _ZERO_RATE_CAUTION:
        levels.append(SuitabilityLevel.CAUTION)
        notes.append(SuitabilityNote(NOTE_HIGH_ZERO_RATE, {"zero_rate": metrics.zero_rate}))
    if metrics.negative_rate > _NEGATIVE_RATE_CAUTION:
        levels.append(SuitabilityLevel.CAUTION)
        notes.append(
            SuitabilityNote(NOTE_HIGH_NEGATIVE_RATE, {"negative_rate": metrics.negative_rate})
        )
    if metrics.missing_rate > _MISSING_RATE_CAUTION:
        levels.append(SuitabilityLevel.CAUTION)
        notes.append(
            SuitabilityNote(NOTE_HIGH_MISSING_RATE, {"missing_rate": metrics.missing_rate})
        )

    if SuitabilityLevel.DIFFICULT in levels:
        overall = SuitabilityLevel.DIFFICULT
    elif SuitabilityLevel.CAUTION in levels:
        overall = SuitabilityLevel.CAUTION
    else:
        overall = SuitabilityLevel.GOOD

    return SuitabilityAssessment(level=overall, metrics=metrics, notes=notes)
