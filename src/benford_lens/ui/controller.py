"""Framework-agnostic session state and workflow orchestration.

Deliberately has no PySide6 import: MainWindow is a thin wrapper around
this controller so the workflow logic stays independently testable.
"""

from __future__ import annotations

from collections.abc import Hashable
from dataclasses import dataclass, field, replace

import pandas as pd

from benford_lens.analysis.benford import BenfordResult, analyze_first_digit, first_digit
from benford_lens.analysis.preprocessing import (
    PreprocessingOptions,
    PreprocessingPreview,
    apply_preprocessing,
)
from benford_lens.analysis.suitability import (
    SuitabilityAssessment,
    assess_suitability,
    compute_suitability_metrics,
)
from benford_lens.io.csv_loader import load_csv
from benford_lens.io.excel_loader import list_sheets, load_excel


@dataclass
class SessionState:
    dataframe: pd.DataFrame | None = None
    # pandas column labels are not guaranteed to be str — pd.read_excel can
    # yield int (or other hashable) labels for numeric header cells, so this
    # must accept anything that can appear as a DataFrame column label.
    selected_column: Hashable | None = None
    preprocessing_options: PreprocessingOptions = field(default_factory=PreprocessingOptions)
    last_result: BenfordResult | None = None
    # Snapshots of everything that went into `last_result`, captured by
    # analyze() from one single preprocessing pass. Report export must read
    # these rather than re-deriving from live panel/controller state, which
    # the user may have changed since the analysis ran.
    last_preprocessing_options: PreprocessingOptions | None = None
    last_preprocessing_preview: PreprocessingPreview | None = None
    last_suitability: SuitabilityAssessment | None = None


class SessionController:
    def __init__(self) -> None:
        self.state: SessionState = SessionState()

    def open_csv(self, path: str) -> pd.DataFrame:
        self.state = SessionState(dataframe=load_csv(path))
        return self.state.dataframe

    def list_excel_sheets(self, path: str) -> list[str]:
        return list_sheets(path)

    def open_excel(self, path: str, sheet_name: str) -> pd.DataFrame:
        self.state = SessionState(dataframe=load_excel(path, sheet_name))
        return self.state.dataframe

    def column_names(self) -> list[Hashable]:
        if self.state.dataframe is None:
            return []
        return list(self.state.dataframe.columns)

    def select_column(self, column: Hashable) -> None:
        if self.state.dataframe is None or column not in self.state.dataframe.columns:
            raise ValueError(f"Unknown column: {column}")
        self.state.selected_column = column

    def analyze(self) -> BenfordResult:
        # One preprocessing pass feeds the result, the preview and the
        # suitability metrics, so the three can never disagree with each
        # other or with the chart the user is looking at.
        raw_series = self._raw_selected_series()
        options = self.state.preprocessing_options
        numeric_series, preview = apply_preprocessing(raw_series, options)
        result = analyze_first_digit(numeric_series)
        assessment = assess_suitability(compute_suitability_metrics(numeric_series, raw_series))

        self.state.last_result = result
        self.state.last_preprocessing_options = replace(options)
        self.state.last_preprocessing_preview = preview
        self.state.last_suitability = assessment
        return result

    def configure_preprocessing(self, options: PreprocessingOptions) -> PreprocessingPreview:
        self.state.preprocessing_options = options
        _series, preview = apply_preprocessing(self._raw_selected_series(), options)
        return preview

    def _raw_selected_series(self) -> pd.Series:
        if self.state.dataframe is None or self.state.selected_column is None:
            raise ValueError("A file and column must be selected before analysis.")
        return self.state.dataframe[self.state.selected_column]

    def _preprocessed_series(self) -> pd.Series:
        series, _preview = apply_preprocessing(
            self._raw_selected_series(), self.state.preprocessing_options
        )
        return series

    def check_suitability(self) -> SuitabilityAssessment:
        metrics = compute_suitability_metrics(
            self._preprocessed_series(), self._raw_selected_series()
        )
        return assess_suitability(metrics)

    def drill_down(self, digit: int) -> pd.DataFrame:
        assert self.state.dataframe is not None  # narrowed by _preprocessed_series below
        preprocessed_series = self._preprocessed_series()
        digits = preprocessed_series.map(first_digit)
        matching_index = digits[digits == digit].index
        return self.state.dataframe.loc[matching_index]
