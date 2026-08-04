import pytest

from benford_lens.ui.controller import SessionController


def _write_csv(tmp_path):
    path = tmp_path / "data.csv"
    path.write_text("name,amount\nalice,111\nbob,222\ncarol,111\n", encoding="utf-8")
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
