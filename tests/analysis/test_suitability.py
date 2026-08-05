import pandas as pd

from benford_lens.analysis.suitability import (
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
    assert any("zero" in note.lower() for note in assessment.notes)


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
