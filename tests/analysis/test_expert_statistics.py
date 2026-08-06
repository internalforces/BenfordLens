import math

import numpy as np
import pandas as pd
import pytest
from scipy.stats import chisquare, kstest

from benford_lens.analysis.benford import analyze_first_digit
from benford_lens.analysis.expert_statistics import calculate_expert_statistics


def test_calculate_expert_statistics_matches_reference_formulas():
    series = pd.Series([1.2, 2.5, 2.9, 9.1])
    result = analyze_first_digit(series)

    statistics = calculate_expert_statistics(series, result)

    observed = np.array([result.observed_counts[digit] for digit in range(1, 10)])
    expected = np.array([result.expected_proportions[digit] for digit in range(1, 10)])
    expected_counts = expected * result.sample_size
    chi_square = chisquare(observed, expected_counts)
    log_mantissas = np.mod(np.log10(np.abs(series.to_numpy())), 1.0)
    ks = kstest(log_mantissas, "uniform")

    assert statistics.sample_size == 4
    assert statistics.mean_absolute_deviation == pytest.approx(
        np.mean(
            [
                abs(result.observed_proportions[digit] - result.expected_proportions[digit])
                for digit in range(1, 10)
            ]
        )
    )
    assert statistics.chi_square_statistic == pytest.approx(chi_square.statistic)
    assert statistics.chi_square_p_value == pytest.approx(chi_square.pvalue)
    assert statistics.ks_statistic == pytest.approx(ks.statistic)
    assert statistics.ks_p_value == pytest.approx(ks.pvalue)


def test_ks_uses_absolute_nonzero_finite_values_like_first_digit_analysis():
    series = pd.Series([-12.0, 0.0, 340.0, math.nan, math.inf])
    result = analyze_first_digit(series)

    statistics = calculate_expert_statistics(series, result)

    expected_ks = kstest(np.mod(np.log10(np.array([12.0, 340.0])), 1.0), "uniform")
    assert statistics.sample_size == 2
    assert statistics.ks_statistic == pytest.approx(expected_ks.statistic)
    assert statistics.ks_p_value == pytest.approx(expected_ks.pvalue)


def test_empty_analysis_has_no_inferential_statistics():
    series = pd.Series([], dtype=float)

    statistics = calculate_expert_statistics(series, analyze_first_digit(series))

    assert statistics.sample_size == 0
    assert statistics.mean_absolute_deviation is None
    assert statistics.chi_square_statistic is None
    assert statistics.chi_square_p_value is None
    assert statistics.ks_statistic is None
    assert statistics.ks_p_value is None
