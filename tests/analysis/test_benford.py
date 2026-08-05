import math

import pandas as pd
import pytest

from benford_lens.analysis.benford import (
    analyze_first_digit,
    expected_first_digit_distribution,
    first_digit,
)


def test_expected_distribution_matches_benfords_law():
    expected = expected_first_digit_distribution()

    assert set(expected.keys()) == set(range(1, 10))
    assert expected[1] == pytest.approx(math.log10(2))
    assert sum(expected.values()) == pytest.approx(1.0)


@pytest.mark.parametrize(
    "value,expected",
    [
        (123.45, 1),
        (45.0, 4),
        (0.0034, 3),
        (-789, 7),
        (7, 7),
        (0, None),
        (None, None),
        (float("nan"), None),
        (float("inf"), None),
        (float("-inf"), None),
    ],
)
def test_first_digit_extracts_leading_significant_digit(value, expected):
    assert first_digit(value) == expected


def test_analyze_first_digit_counts_and_proportions():
    series = pd.Series([111, 111, 222, None, 0])

    result = analyze_first_digit(series)

    assert result.sample_size == 3
    assert result.observed_counts[1] == 2
    assert result.observed_counts[2] == 1
    assert result.observed_proportions[1] == pytest.approx(2 / 3)
    assert result.expected_proportions == expected_first_digit_distribution()


def test_analyze_first_digit_handles_empty_series():
    result = analyze_first_digit(pd.Series([], dtype=float))

    assert result.sample_size == 0
    assert result.observed_proportions[1] == 0.0
