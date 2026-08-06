from dataclasses import FrozenInstanceError

import pandas as pd
import pytest

from benford_lens.analysis.benford import CombinedBenfordResult, DigitPosition
from benford_lens.analysis.preprocessing import PreprocessingOptions
from benford_lens.analysis.suitability import SuitabilityLevel
from benford_lens.ui.controller import AnalysisMode, SessionController


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
    assert controller.state.last_expert_statistics is not None
    assert controller.state.last_expert_statistics.sample_size == result.sample_size


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


def test_analyze_snapshots_the_options_preview_and_suitability_it_used(tmp_path):
    # Regression test: report export needs the preprocessing options, the
    # preview counts and the suitability assessment that produced
    # last_result — not whatever the user selected afterwards.
    path = tmp_path / "with_negative.csv"
    path.write_text("amount\n-111\n222\n0\n", encoding="utf-8")
    controller = SessionController()
    controller.open_csv(str(path))
    controller.select_column("amount")
    controller.configure_preprocessing(PreprocessingOptions(negative_handling="absolute"))

    result = controller.analyze()

    state = controller.state
    assert state.last_preprocessing_options is not None
    assert state.last_preprocessing_options.negative_handling == "absolute"
    assert state.last_preprocessing_preview is not None
    assert state.last_preprocessing_preview.total_after == result.sample_size == 2
    assert state.last_suitability is not None
    assert state.last_suitability.metrics.sample_count == 2
    assert state.last_expert_statistics is not None
    assert state.last_expert_statistics.sample_size == 2
    snapshot = state.analysis_snapshot
    assert snapshot is not None

    # Changing the live options invalidates the displayed/exportable snapshot,
    # while the immutable object already returned remains unchanged.
    controller.configure_preprocessing(PreprocessingOptions(negative_handling="exclude"))

    assert state.analysis_snapshot is None
    assert snapshot.preprocessing_options.negative_handling == "absolute"
    assert snapshot.preprocessing_preview.total_after == 2
    assert snapshot.suitability.metrics.sample_count == 2


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


def test_open_excel_records_the_sheet_name_and_csv_leaves_it_none(tmp_path):
    # The exported report has to be able to say which sheet was analyzed.
    controller = SessionController()

    controller.open_excel(_write_excel_with_numeric_headers(tmp_path), sheet_name="Sheet1")
    assert controller.state.sheet_name == "Sheet1"

    controller.open_csv(_write_csv(tmp_path))
    assert controller.state.sheet_name is None


def test_second_digit_mode_returns_second_digit_result_and_snapshot(tmp_path):
    path = tmp_path / "second.csv"
    path.write_text("amount\n101\n111\n222\n5\n", encoding="utf-8")
    controller = SessionController()
    controller.open_csv(str(path))
    controller.select_column("amount")

    result = controller.analyze(AnalysisMode.SECOND)

    assert result.observed_counts[0] == 2
    assert result.observed_counts[1] == 1
    assert result.observed_counts[2] == 1
    assert controller.state.analysis_mode is AnalysisMode.SECOND
    assert controller.state.analysis_snapshot is not None
    assert controller.state.analysis_snapshot.mode is AnalysisMode.SECOND


def test_combined_mode_snapshots_both_results_and_shared_statistics(tmp_path):
    controller = SessionController()
    controller.open_csv(_write_csv(tmp_path))
    controller.select_column("amount")

    result = controller.analyze(AnalysisMode.COMBINED)

    assert isinstance(result, CombinedBenfordResult)
    assert result.first.observed_counts[1] == 2
    assert result.second.observed_counts[1] == 2
    snapshot = controller.state.analysis_snapshot
    assert snapshot is not None
    assert snapshot.result is result
    assert snapshot.mode is AnalysisMode.COMBINED
    assert snapshot.expert_statistics.log_mantissa.sample_size == 3


@pytest.mark.parametrize("mode", list(AnalysisMode))
def test_each_analysis_mode_preprocesses_exactly_once(tmp_path, monkeypatch, mode):
    from benford_lens.analysis.preprocessing import apply_preprocessing as real_apply

    calls = 0

    def counting_apply(raw_series, options):
        nonlocal calls
        calls += 1
        return real_apply(raw_series, options)

    monkeypatch.setattr("benford_lens.ui.controller.apply_preprocessing", counting_apply)
    controller = SessionController()
    controller.open_csv(_write_csv(tmp_path))
    controller.select_column("amount")

    controller.analyze(mode)

    assert calls == 1


@pytest.mark.parametrize("mode", list(AnalysisMode))
def test_each_analysis_mode_extracts_digits_once_per_preprocessed_value(
    tmp_path, monkeypatch, mode
):
    from benford_lens.analysis import benford

    real_extract = benford._significant_digits
    calls = 0

    def counting_extract(value):
        nonlocal calls
        calls += 1
        return real_extract(value)

    monkeypatch.setattr(benford, "_significant_digits", counting_extract)
    controller = SessionController()
    controller.open_csv(_write_csv(tmp_path))
    controller.select_column("amount")

    controller.analyze(mode)

    assert calls == 3


def test_analysis_snapshot_is_frozen(tmp_path):
    controller = SessionController()
    controller.open_csv(_write_csv(tmp_path))
    controller.select_column("amount")
    controller.analyze()
    snapshot = controller.state.analysis_snapshot
    assert snapshot is not None

    with pytest.raises(FrozenInstanceError):
        snapshot.mode = AnalysisMode.SECOND


def test_source_column_options_and_mode_changes_invalidate_snapshot(tmp_path):
    path = tmp_path / "two_columns.csv"
    path.write_text("amount,other\n111,333\n222,444\n", encoding="utf-8")
    controller = SessionController()
    controller.open_csv(str(path))
    controller.select_column("amount")
    controller.analyze()

    controller.select_column("other")
    assert controller.state.analysis_snapshot is None

    controller.analyze()
    controller.configure_preprocessing(PreprocessingOptions(negative_handling="exclude"))
    assert controller.state.analysis_snapshot is None

    controller.analyze()
    controller.set_analysis_mode(AnalysisMode.SECOND)
    assert controller.state.analysis_snapshot is None

    controller.analyze()
    controller.open_csv(str(path))
    assert controller.state.analysis_snapshot is None


def test_position_aware_drill_down_uses_stored_mapping_and_original_rows(tmp_path):
    path = tmp_path / "drill_both.csv"
    path.write_text(
        "name,amount\nalice,101\nbob,111\ncarol,-105\ndave,222\n",
        encoding="utf-8",
    )
    controller = SessionController()
    controller.open_csv(str(path))
    controller.select_column("amount")
    controller.analyze(AnalysisMode.COMBINED)

    first_rows = controller.drill_down_digit(DigitPosition.FIRST, 1)
    second_rows = controller.drill_down_digit(DigitPosition.SECOND, 0)

    assert list(first_rows["name"]) == ["alice", "bob", "carol"]
    assert list(second_rows["name"]) == ["alice", "carol"]
    assert list(second_rows["amount"]) == [101, -105]


def test_drill_down_rejects_position_not_in_current_mode(tmp_path):
    controller = SessionController()
    controller.open_csv(_write_csv(tmp_path))
    controller.select_column("amount")
    controller.analyze(AnalysisMode.SECOND)

    with pytest.raises(ValueError, match="does not include first-digit"):
        controller.drill_down_digit(DigitPosition.FIRST, 1)
