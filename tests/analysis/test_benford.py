import math

import pandas as pd
import pytest

from benford_lens.analysis.benford import (
    CombinedBenfordResult,
    DigitPosition,
    analyze_combined,
    analyze_combined_with_digit_pairs,
    analyze_first_digit,
    analyze_second_digit,
    expected_first_digit_distribution,
    expected_second_digit_distribution,
    first_digit,
    second_digit,
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


def test_digit_position_values_are_stable():
    assert DigitPosition.FIRST.value == "first"
    assert DigitPosition.SECOND.value == "second"


@pytest.mark.parametrize(
    "value,expected",
    [
        (123.45, 2),
        (105, 0),
        (5, 0),
        (0.0034, 4),
        (-789, 8),
        (9.99, 9),
        (1e20, 0),
        (0, None),
        (None, None),
        (float("nan"), None),
        (float("inf"), None),
        (float("-inf"), None),
    ],
)
def test_second_digit_extracts_second_significant_digit(value, expected):
    assert second_digit(value) == expected


def test_expected_second_digit_distribution_matches_reference_values():
    expected = expected_second_digit_distribution()

    reference = [
        0.11968,
        0.11389,
        0.10882,
        0.10433,
        0.10031,
        0.09668,
        0.09337,
        0.09035,
        0.08757,
        0.08500,
    ]
    assert set(expected) == set(range(10))
    assert [expected[digit] for digit in range(10)] == pytest.approx(reference, abs=5e-6)
    assert sum(expected.values()) == pytest.approx(1.0)


def test_analyze_second_digit_counts_and_proportions():
    result = analyze_second_digit(pd.Series([101, 111, 222, 5, None, 0]))

    assert result.sample_size == 4
    assert result.observed_counts[0] == 2
    assert result.observed_counts[1] == 1
    assert result.observed_counts[2] == 1
    assert result.observed_proportions[0] == pytest.approx(0.5)
    assert result.expected_proportions == expected_second_digit_distribution()


def test_analyze_second_digit_handles_empty_series():
    result = analyze_second_digit(pd.Series([], dtype=float))

    assert result.sample_size == 0
    assert set(result.observed_counts) == set(range(10))
    assert all(proportion == 0.0 for proportion in result.observed_proportions.values())


class _OneShotValues:
    def __init__(self, values):
        self._values = values
        self.iterations = 0

    def __iter__(self):
        self.iterations += 1
        if self.iterations > 1:
            raise AssertionError("combined analysis iterated over the source more than once")
        return iter(self._values)


def test_analyze_combined_matches_independent_results_in_one_source_iteration():
    values = [123.45, 105, -789, 0.0034, 5, None, 0, float("nan")]
    one_shot_values = _OneShotValues(values)

    combined = analyze_combined(one_shot_values)

    assert isinstance(combined, CombinedBenfordResult)
    assert combined.first == analyze_first_digit(values)
    assert combined.second == analyze_second_digit(values)
    assert one_shot_values.iterations == 1


def test_combined_digit_pairs_stay_aligned_with_invalid_values():
    values = [123.0, None, 0, 5.0, float("nan"), -789.0]

    result, digit_pairs = analyze_combined_with_digit_pairs(values)

    assert result == analyze_combined(values)
    assert digit_pairs == ((1, 2), None, None, (5, 0), None, (7, 8))
