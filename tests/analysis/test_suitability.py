from pathlib import Path

import pandas as pd

from benford_lens.analysis import suitability
from benford_lens.analysis.benford import MIN_MEANINGFUL_SAMPLE
from benford_lens.analysis.suitability import (
    NOTE_HIGH_MISSING_RATE,
    NOTE_HIGH_NEGATIVE_RATE,
    NOTE_HIGH_ZERO_RATE,
    NOTE_SAMPLE_TOO_SMALL,
    SuitabilityLevel,
    assess_suitability,
    compute_suitability_metrics,
)


def test_small_sample_is_difficult():
    raw = pd.Series(range(10))
    preprocessed = pd.Series(range(10), dtype=float)

    metrics = compute_suitability_metrics(preprocessed, raw)
    assessment = assess_suitability(metrics)

    assert metrics.sample_count == 10
    assert assessment.level is SuitabilityLevel.DIFFICULT


def test_moderate_sample_and_narrow_magnitude_range_is_caution():
    raw = pd.Series(range(1, 101))
    # 1..100, spans 3 digit buckets (1-digit, 2-digit, 3-digit)
    preprocessed = pd.Series(range(1, 101), dtype=float)

    metrics = compute_suitability_metrics(preprocessed, raw)
    assessment = assess_suitability(metrics)

    assert metrics.sample_count == 100
    assert metrics.digit_range == 3
    assert assessment.level is SuitabilityLevel.CAUTION


def test_large_diverse_multi_magnitude_sample_is_good():
    values = [float(v) for v in range(1, 301)] + [3000.0, 30000.0, 300000.0]
    raw = pd.Series(values)
    preprocessed = pd.Series(values)

    metrics = compute_suitability_metrics(preprocessed, raw)
    assessment = assess_suitability(metrics)

    assert metrics.digit_range >= 4
    assert assessment.level is SuitabilityLevel.GOOD


def test_single_order_of_magnitude_is_difficult_regardless_of_sample_size():
    values = [float(v) for v in range(10, 100)] * 5  # 450 values, all 2-digit
    raw = pd.Series(values)
    preprocessed = pd.Series(values)

    metrics = compute_suitability_metrics(preprocessed, raw)
    assessment = assess_suitability(metrics)

    assert metrics.sample_count >= 300
    assert metrics.digit_range == 1
    assert assessment.level is SuitabilityLevel.DIFFICULT


def test_high_zero_rate_in_raw_data_adds_a_caution_note():
    raw = pd.Series([0] * 40 + list(range(1, 61)))
    preprocessed = pd.Series(range(1, 61), dtype=float)  # zeros already excluded upstream

    metrics = compute_suitability_metrics(preprocessed, raw)
    assessment = assess_suitability(metrics)

    assert metrics.zero_rate > 0.3
    codes = [note.code for note in assessment.notes]
    assert NOTE_HIGH_ZERO_RATE in codes
    note = next(n for n in assessment.notes if n.code == NOTE_HIGH_ZERO_RATE)
    assert note.params["zero_rate"] == metrics.zero_rate


def test_missing_rate_is_computed_against_raw_series():
    raw = pd.Series([1, 2, None, None, 5])
    preprocessed = pd.Series([1.0, 2.0, 5.0])

    metrics = compute_suitability_metrics(preprocessed, raw)

    assert metrics.missing_rate == 0.4


def test_distinct_value_count_and_duplicate_rate():
    raw = pd.Series([1, 1, 1, 2, 3])
    preprocessed = pd.Series([1.0, 1.0, 1.0, 2.0, 3.0])

    metrics = compute_suitability_metrics(preprocessed, raw)

    assert metrics.distinct_value_count == 3
    assert metrics.duplicate_rate == 0.4  # 1 - 3/5


def test_high_negative_rate_adds_a_caution_note_about_negative_handling():
    # Regression test: the negative_rate > _NEGATIVE_RATE_CAUTION branch in
    # assess_suitability() had no test exercising it before this change.
    values = [float(v) for v in range(1, 301)] + [3000.0, 30000.0, 300000.0]
    raw = pd.Series([-v for v in values[:200]] + values[200:])  # >50% negative
    preprocessed = pd.Series(values)  # negatives already handled upstream

    metrics = compute_suitability_metrics(preprocessed, raw)
    assessment = assess_suitability(metrics)

    assert metrics.negative_rate > 0.5
    assert NOTE_HIGH_NEGATIVE_RATE in [note.code for note in assessment.notes]


def test_high_missing_rate_adds_a_caution_note():
    # Regression test: the missing_rate > _MISSING_RATE_CAUTION branch in
    # assess_suitability() had no test exercising it before this change
    # (the existing missing-rate test only checked compute_suitability_metrics,
    # never assess_suitability's notes).
    values = [float(v) for v in range(1, 301)] + [3000.0, 30000.0, 300000.0]
    raw = pd.Series(values + [None] * 150)  # >30% blank
    preprocessed = pd.Series(values)

    metrics = compute_suitability_metrics(preprocessed, raw)
    assessment = assess_suitability(metrics)

    assert metrics.missing_rate > 0.3
    assert NOTE_HIGH_MISSING_RATE in [note.code for note in assessment.notes]


def test_notes_carry_codes_and_params_not_prose():
    # The Analysis Engine must not originate user-facing strings (AGENTS.md);
    # notes are structured so the presentation layer can translate them.
    raw = pd.Series(range(10))
    preprocessed = pd.Series(range(10), dtype=float)

    assessment = assess_suitability(compute_suitability_metrics(preprocessed, raw))

    codes = [note.code for note in assessment.notes]
    assert NOTE_SAMPLE_TOO_SMALL in codes
    too_small = next(n for n in assessment.notes if n.code == NOTE_SAMPLE_TOO_SMALL)
    assert too_small.params == {"sample_count": 10, "minimum": MIN_MEANINGFUL_SAMPLE}


def test_suitability_module_contains_no_user_facing_prose():
    # Guard for the architecture rule: every note is a code plus numbers, so
    # no English sentence should be constructed anywhere in this module.
    source = Path(suitability.__file__).read_text(encoding="utf-8")
    for phrase in ("valid value", "orders of magnitude", "source values were", "sample size."):
        assert phrase not in source
