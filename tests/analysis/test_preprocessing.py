import math

import pandas as pd

from benford_lens.analysis.preprocessing import PreprocessingOptions, apply_preprocessing


def test_defaults_convert_negative_to_absolute_and_exclude_zero():
    series = pd.Series([-5, 0, 10])

    result, preview = apply_preprocessing(series, PreprocessingOptions())

    assert list(result) == [5.0, 10.0]
    assert preview.total_before == 3
    assert preview.total_after == 2
    assert preview.excluded_negative == 0
    assert preview.excluded_zero == 1


def test_negative_handling_exclude_drops_negative_values():
    series = pd.Series([-5, 10])
    options = PreprocessingOptions(negative_handling="exclude")

    result, preview = apply_preprocessing(series, options)

    assert list(result) == [10.0]
    assert preview.excluded_negative == 1


def test_negative_handling_keep_leaves_negative_values_untouched():
    series = pd.Series([-5, 10])
    options = PreprocessingOptions(negative_handling="keep")

    result, _preview = apply_preprocessing(series, options)

    assert list(result) == [-5.0, 10.0]


def test_zero_handling_keep_retains_zero():
    series = pd.Series([0, 10])
    options = PreprocessingOptions(zero_handling="keep")

    result, preview = apply_preprocessing(series, options)

    assert list(result) == [0.0, 10.0]
    assert preview.excluded_zero == 0


def test_decimal_handling_round_and_truncate():
    series = pd.Series([3.7, 10])

    rounded, _ = apply_preprocessing(series, PreprocessingOptions(decimal_handling="round"))
    truncated, _ = apply_preprocessing(series, PreprocessingOptions(decimal_handling="truncate"))

    assert list(rounded) == [4.0, 10.0]
    assert list(truncated) == [3.0, 10.0]


def test_decimal_rounding_before_zero_exclusion_prevents_silent_reintroduction():
    """Regression: values that round to zero should be excluded by zero_handling."""
    series = pd.Series([0.4, 10])
    options = PreprocessingOptions(zero_handling="exclude", decimal_handling="round")

    result, preview = apply_preprocessing(series, options)

    # 0.4 rounds to 0.0, which is then excluded by zero_handling="exclude"
    assert list(result) == [10.0]
    assert preview.excluded_zero == 1


def test_blank_values_are_excluded_and_counted():
    series = pd.Series([10, None, 20])

    result, preview = apply_preprocessing(series, PreprocessingOptions())

    assert list(result) == [10.0, 20.0]
    assert preview.excluded_blank == 1


def test_string_to_number_strips_currency_formatting():
    series = pd.Series(["1,200원", "$100", 50])

    result, preview = apply_preprocessing(series, PreprocessingOptions())

    assert list(result) == [1200.0, 100.0, 50.0]
    assert preview.excluded_non_numeric == 0


def test_string_to_number_disabled_treats_currency_strings_as_non_numeric():
    series = pd.Series(["1,200원", 50])
    options = PreprocessingOptions(string_to_number=False)

    result, preview = apply_preprocessing(series, options)

    assert list(result) == [50.0]
    assert preview.excluded_non_numeric == 1


def test_duplicate_handling_exclude_keeps_first_occurrence_only():
    series = pd.Series([10, 10, 20])
    options = PreprocessingOptions(duplicate_handling="exclude")

    result, _preview = apply_preprocessing(series, options)

    assert list(result) == [10.0, 20.0]


def test_duplicate_handling_keep_is_the_default():
    series = pd.Series([10, 10, 20])

    result, _preview = apply_preprocessing(series, PreprocessingOptions())

    assert list(result) == [10.0, 10.0, 20.0]


def test_preview_samples_are_capped_and_reflect_before_after():
    series = pd.Series(range(20))

    _result, preview = apply_preprocessing(series, PreprocessingOptions())

    assert len(preview.sample_before) == 5
    assert preview.sample_before == [0, 1, 2, 3, 4]
    assert math.isclose(preview.sample_after[0], 1.0)


def test_infinite_values_are_excluded_and_counted_as_non_numeric():
    # Regression test: inf is not NaN, so it survived the blank/non-numeric
    # exclusion and reached math.trunc(), raising an uncaught OverflowError
    # from inside the Analyze and Preview handlers.
    series = pd.Series([111.0, float("inf"), float("-inf"), 222.0])

    result, preview = apply_preprocessing(series, PreprocessingOptions(decimal_handling="truncate"))

    assert list(result) == [111.0, 222.0]
    assert preview.total_before == 4
    assert preview.total_after == 2
    assert preview.excluded_non_numeric == 2
    assert preview.excluded_blank == 0


def test_the_literal_string_inf_is_excluded_too():
    # pd.to_numeric coerces the string "inf" to float infinity, so a text
    # column can carry one in without any float ever being typed.
    series = pd.Series(["111", "inf", "222"])

    result, preview = apply_preprocessing(series, PreprocessingOptions(decimal_handling="truncate"))

    assert list(result) == [111.0, 222.0]
    assert preview.excluded_non_numeric == 1
