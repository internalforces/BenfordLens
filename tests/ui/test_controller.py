import pandas as pd
import pytest

from benford_lens.analysis.preprocessing import PreprocessingOptions
from benford_lens.analysis.suitability import SuitabilityLevel
from benford_lens.ui.controller import SessionController


def _write_csv(tmp_path):
    path = tmp_path / "data.csv"
    path.write_text("name,amount\nalice,111\nbob,222\ncarol,111\n", encoding="utf-8")
    return str(path)


def _write_excel_with_numeric_headers(tmp_path):
    # Regression fixture for Finding 1: a sheet whose header row is numeric
    # (e.g. year columns) makes pandas assign non-string int column labels,
    # not str labels the way every CSV column always is.
    path = tmp_path / "numeric_headers.xlsx"
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        pd.DataFrame({2021: [111, 111, 222], 2022: [4, 5, 6]}).to_excel(
            writer, sheet_name="Sheet1", index=False
        )
    return str(path)


def test_open_csv_loads_dataframe_and_resets_selection(tmp_path):
    controller = SessionController()

    df = controller.open_csv(_write_csv(tmp_path))

    assert list(df.columns) == ["name", "amount"]
    assert controller.state.selected_column is None
    assert controller.column_names() == ["name", "amount"]


def test_select_column_requires_an_existing_column(tmp_path):
    controller = SessionController()
    controller.open_csv(_write_csv(tmp_path))

    with pytest.raises(ValueError):
        controller.select_column("does_not_exist")

    controller.select_column("amount")
    assert controller.state.selected_column == "amount"


def test_analyze_requires_file_and_column_selected():
    controller = SessionController()

    with pytest.raises(ValueError):
        controller.analyze()


def test_analyze_runs_first_digit_benford_on_selected_column(tmp_path):
    controller = SessionController()
    controller.open_csv(_write_csv(tmp_path))
    controller.select_column("amount")

    result = controller.analyze()

    assert result.sample_size == 3
    assert result.observed_counts[1] == 2
    assert result.observed_counts[2] == 1
    assert controller.state.last_result is result


def test_column_names_is_empty_before_any_file_is_opened():
    controller = SessionController()

    assert controller.column_names() == []


def test_configure_preprocessing_returns_a_preview(tmp_path):
    controller = SessionController()
    controller.open_csv(_write_csv(tmp_path))
    controller.select_column("amount")

    preview = controller.configure_preprocessing(PreprocessingOptions(negative_handling="exclude"))

    assert preview.total_before == 3
    assert controller.state.preprocessing_options.negative_handling == "exclude"


def test_analyze_applies_configured_preprocessing(tmp_path):
    path = tmp_path / "with_negative.csv"
    path.write_text("amount\n-111\n222\n0\n", encoding="utf-8")
    controller = SessionController()
    controller.open_csv(str(path))
    controller.select_column("amount")
    controller.configure_preprocessing(PreprocessingOptions(negative_handling="exclude"))

    result = controller.analyze()

    # -111 excluded (negative_handling="exclude"), 0 excluded (default zero
    # handling), leaving only 222 -> sample_size 1, leading digit 2.
    assert result.sample_size == 1
    assert result.observed_counts[2] == 1


def test_open_excel_select_column_and_analyze_end_to_end(tmp_path):
    controller = SessionController()
    xlsx_path = _write_excel_with_numeric_headers(tmp_path)

    df = controller.open_excel(xlsx_path, sheet_name="Sheet1")

    assert list(df.columns) == [2021, 2022]
    assert controller.column_names() == [2021, 2022]

    # Regression coverage for Finding 1: selecting a numeric-labeled column
    # (not a string) must succeed, since pd.read_excel can yield int column
    # labels for numeric header cells.
    controller.select_column(2021)
    assert controller.state.selected_column == 2021

    result = controller.analyze()

    assert result.sample_size == 3
    assert result.observed_counts[1] == 2
    assert result.observed_counts[2] == 1


def test_check_suitability_returns_an_assessment(tmp_path):
    path = tmp_path / "small.csv"
    path.write_text("amount\n" + "\n".join(str(v) for v in range(1, 11)) + "\n", encoding="utf-8")
    controller = SessionController()
    controller.open_csv(str(path))
    controller.select_column("amount")

    assessment = controller.check_suitability()

    assert assessment.metrics.sample_count == 10
    assert assessment.level is SuitabilityLevel.DIFFICULT


def test_drill_down_returns_original_rows_matching_the_leading_digit(tmp_path):
    path = tmp_path / "drill.csv"
    path.write_text("name,amount\nalice,111\nbob,222\ncarol,-155\n", encoding="utf-8")
    controller = SessionController()
    controller.open_csv(str(path))
    controller.select_column("amount")
    controller.analyze()  # default preprocessing: negative -> absolute, so -155 -> 155

    rows = controller.drill_down(1)

    assert list(rows["name"]) == ["alice", "carol"]
    assert list(rows["amount"]) == [111, -155]  # original raw values, not preprocessed
